from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('create', views.PostCreateView.as_view(), name='new-post'),
    path('update/<int:pk>', views.PostUpdateView.as_view(), name='post-update'),
    path('p/<str:slug>', views.post_content, name='post-detail'),
    path('faq', views.faq_page, name='faq'),
    path('img/<str:f_type>/<int:pk>', views.download, name='download'),
]
