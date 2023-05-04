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
            cafe = Cafe.objects.get(id=event['cafe'])
            pros = event['pros']
            table_id = event['table_id']
            products = []
            for p in pros:
                pro = Products.objects.get(id=p)
                products.append(pro)

            if products:
                new_order = Order.objects.create(cafe=cafe, table=table_id)
                for prod in products:
                    status = False
                    for pr in new_order.prods.all():
                        if pr.prod.id == prod.id:
                            status = True
                    if status == 0:
                        n_order_p = OrderProd.objects.create(prod=prod, number=1)
                        new_order.prods.add(n_order_p)
                    else:
                        for p in new_order.prods.all():
                            if prod.id == p.prod.id:
                                p.number += 1
                                p.save()

                    new_order.price += prod.price

                new_order.save()
                price = new_order.price

                # Send message to WebSocket
                self.send(text_data=json.dumps({
                    'action': 'addOrder',
                    'order': new_order.id,
                    'oTable': new_order.table,
                    'time': f'{new_order.created.time().strftime("%I:%M %p")}',
                    'price': price,
                }))
                for pro in new_order.prods.all():
                    self.send(text_data=json.dumps({
                        'action': 'addProducts',
                        'order': new_order.id,
                        'pName': pro.prod.name,
                        'pNumber': pro.number,
                        'pPrice': pro.prod.price
                    }))
                self.send(text_data=json.dumps({
                    'action': 'loaded',
                }))
        elif action == 'closeCart':
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
