from django.contrib.auth import views as auth_views
from django.urls import path


from . import views




app_name = "store"


urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path(
        "products/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),


    # Authentication
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="store/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    # Shopping cart
    path("cart/", views.cart_detail, name="cart"),
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "cart/increase/<int:product_id>/",
        views.increase_cart_quantity,
        name="increase_cart_quantity",
    ),
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_cart_quantity,
        name="decrease_cart_quantity",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    
    path(
    "order-success/", 
    views.order_success, 
    name="order_success"
    ),
]
