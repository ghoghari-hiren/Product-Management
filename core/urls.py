from django.urls import path
from .views import RegisterView, LoginView, ProductCreateView, ManageProductView


urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("product", ProductCreateView.as_view(), name="product"),
    path('products/<int:pk>', ManageProductView.as_view(), name='product-manage'),
]