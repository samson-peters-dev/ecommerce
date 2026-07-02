from django.urls import path

from . import views
urlpatterns = [
    # category
    path('category/', views.CategoryCreateRetrieveView.as_view()),
    path('category/<str:id>/', views.CategoryRUDView.as_view()),
    # product
    path('product/', views.ProductCreateRetrieveView.as_view()),
    path('product/<str:id>/', views.ProductRUDView.as_view()),
    # cart
    path('addtocart/<str:id>/', views.AddToCartView.as_view()),
    # users cart
    path('usercart/', views.MyCartView.as_view()),
    # manage cart
    path('manage/<str:id>/', views.ManageCartView.as_view()),
    # checkout
    path('checkout/', views.CheckoutCartView.as_view()),
    # payment
    path('payment/<str:id>/', views.PaymentView.as_view(), name="paystack_page"),
    # path('pod/<str:id>/', views.PaymentOnDelieveryView.as_view(), name="pod_page"),
    # verify
    path('<str:ref>/', views.VerifyPaymentView.as_view()),
]