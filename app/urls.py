from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
		path('', views.login_view, name ='hello'),
        path('register/', views.register, name ='register'),
        path('dashboard/', views.dashboard, name ='dashboard'),
        path('orders/', views.orders, name ='orders'),
        path('logout/', views.logout_view, name ='logout'),
        path('profile/', views.change_custom_info, name ='profile'),
        path('change_password/', views.change_password, name ='change_password'),
        path('add_funds/', views.add_funds, name ='add_funds'),
        path('get_category/', views.get_category, name='get_category'),
        path('get_guide_price/', views.get_guide_price, name='get_guide_price'),
        path('submit_order/', views.submit_order, name='submit_order'),

]

