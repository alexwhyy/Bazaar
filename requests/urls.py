from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('item/<pk>/', views.detail, name='detail'),
	path('item/<pk>/<action>', views.item_action, name='item_action'),
	path('create/', views.create, name='create'),
]