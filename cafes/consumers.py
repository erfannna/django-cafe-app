import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Cafe, Products, Order, OrderProd
import asyncio


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        cafe = self.scope["user"].cafe.first()

        # Send message to room group
        if action == 'submit':
            pros = text_data_json['pros']
            table_id = text_data_json['table_id']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': action,
                    'pros': pros,
                    'table_id': table_id,
                    'cafe': cafe.id
                }
            )
        elif action == 'closeCart':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': action,
                    'cNum': text_data_json['cNum'],
                    'cafe': cafe.id
                }
            )
        else:
            o_id = text_data_json['id']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': action,
                    'o_id': o_id,
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        action = event['action']

        if action == 'submit':
            pros = event['pros']
            table_id = event['table_id']
            cafe = Cafe.objects.get(id=event['cafe'])
            prods = []
            add_price = 0

            try:
                new_order = Order.objects.get(cafe=cafe, table=table_id, closed=False)
            except:
                new_order = Order.objects.create(cafe=cafe, table=table_id, closed=False)

            for p in pros:
                prod = Products.objects.get(id=p)
                if prod not in prods:
                    prd = new_order.prods.filter(prod=prod).first()
                    if not prd:
                        n_order_p = OrderProd.objects.create(prod=prod, number=pros.count(prod.id))
                        add_price += pros.count(prod.id) * prod.price
                        new_order.prods.add(n_order_p)
                        prods.append(prod)
                    else:
                        prd.number += pros.count(prod.id)
                        add_price += pros.count(prod.id) * prod.price
                        prd.save()
                        prods.append(prod)

                new_order.price += prod.price
                new_order.save()

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'action': 'addOrder',
                'order': new_order.id,
                'oTable': new_order.table,
                'time': f'{new_order.created.time().strftime("%I:%M %p")}',
                'price': add_price,
            }))

            for pro in prods:
                self.send(text_data=json.dumps({
                    'action': 'addProducts',
                    'order': new_order.id,
                    'pName': pro.name,
                    'pNumber': pros.count(pro.id),
                    'pPrice': pro.price
                }))
            self.send(text_data=json.dumps({
                'action': 'loaded',
            }))

        elif action == 'closeCart':
            cafe = Cafe.objects.get(id=event['cafe'])
            cart = Order.objects.get(cafe=cafe, table=event['cNum'], closed=False)
            cart.closed = True
            cart.save()
            self.send(text_data=json.dumps({
                'action': action,
                'cNum': event['cNum']
            }))

        else:
            o_id = event['o_id']
            Order.objects.filter(id=o_id).delete()
            self.send(text_data=json.dumps({
                'action': 'delete',
                'id': o_id
            }))
