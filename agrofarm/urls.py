"""agrofarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# from django.contrib import admin

from baton.autodiscover import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

handler404 = 'core.views.error404'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('base/', views.Base.as_view(), name="base"),
    path('about_us/', views.AboutUs.as_view(), name="about_us"),
    path('checkout/', views.checkout, name="checkout"),
    path('insert_order/', views.insert_order, name="insert_order"),
    path('contact/', views.Contact.as_view(), name="contact"),
    # path('page/product_details/', views.ProductDetails.as_view(), name="product_details"),
    path('products/', views.Products.as_view(), name="products"),
    path('products/<int:pk>', views.ProductDetails.as_view(), name="products"),
    # path('page/shopping_cart/', views.ShoppingCart.as_view(), name="shopping_cart"),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.Activate.as_view(), name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="core/password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="core/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_done.html"), name ='password_reset_complete'),

    path('user_profile/', views.user_profile, name="user_profile"),
    # path('update_profile<int:id>', views.update_profile,  name="update_profile"),

    path('__debug__/', include(debug_toolbar.urls)),

    path('category/<name>', views.Category.as_view(), name="category"),
    path('search/', views.Search.as_view(), name="category"),

    path('order_history/', views.OrderHistory.as_view(), name="order_history"),
    path('order_history/<int:pk>', views.OrderDetails.as_view(), name="order_history"),
    path('order_report/', views.OrderReport.as_view(), name="order_report"),
    path('order_report/<int:pk>', views.PdfOrderReport, name="pdf_order_report"),
    path('user_info/<int:pk>', views.UserInfo.as_view(), name="user_info"),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('create_pdf/', views.create_pdf, name='create_pdf'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
