from django.urls            import path

from carts.views            import CartView, CartDetailView

urlpatterns = [
    path('', CartView.as_view()),
    path('/<int:cart_id>', CartDetailView.as_view())
]