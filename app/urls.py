from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart', views.cart, name='cart'),
    path('add-cart', views.add_cart, name='add-cart'),
    path('update-cart', views.update_cart, name='update-cart'),
    path('remove-product', views.remove_product, name='remove-product'),
    path('checkout', views.checkout, name='checkout'),
    path('update-wilaya', views.update_wilaya, name='update-wilaya'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('control', views.control, name='control'),
    path('edit-main-interface', views.edit_main_interface, name='edit-main-interface'),
    path('manage-products', views.manage_products, name='manage-products'),
    path('delete-product', views.delete_product, name='delete-product'),
    path('add-product', views.add_product, name='add-product'),
    path('view-orders', views.view_orders, name='view-orders'),
    path('order/<int:id>', views.order, name='order'),
    path('delete-order/<int:id>', views.delete_order, name='delete-order'),
    path('update-sizes', views.update_sizes, name='update-sizes'),
    path('update-product-sizes/<int:id>', views.update_product_sizes, name='update-product-sizes'),
]