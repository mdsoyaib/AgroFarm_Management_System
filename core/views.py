from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# from django.http import HttpResponse
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View, generic

from core.forms import SignUpForm
from core.models import Product, WebsiteInfo, CustomUser, Order, TestOrder, OrderDetail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .cart import Cart
from .forms import CartAddProductForm


class Base(View):
    def get(self, request):
        return render(request, 'core/base.html')


class AboutUs(View):
    def get(self, request):
        info = WebsiteInfo.objects.all()
        return render(request, 'core/about_us.html', {"info": info})


# class Checkout(View):
def checkout(request):
    cart = Cart(request)
    return render(request, 'core/checkout.html', {'cart': cart})


def insert_order(request):
    if request.method == "POST":
        total_price = request.POST["total_price"]
        # email = request.POST["email"]
        user = request.user
        # print(request.POST)
        order = Order(total_price=total_price, customer=user)
        order.save()
        # print(order.id)

        cart = Cart(request)
        cart.clear()
        for item in cart:
            product = item['product']
            quantity = item['quantity']
            price = item['total_price']
            order_details = OrderDetail(quantity=quantity, price=price, product=product, order=order)
            order_details.save()
            messages.success(request, "Your order has been placed successfully..!")
    return redirect(checkout)


class Contact(View):
    def get(self, request):
        info = WebsiteInfo.objects.all()
        return render(request, 'core/contact.html', {"info": info})


class Index(View):
    def get(self, request):
        featured = Product.objects.filter(featured=True, active=True).order_by('-id')
        return render(request, 'core/index.html', {'featured': featured})


class ProductDetails(View):
    def get(self, request, pk):
        p = Product.objects.get(pk=pk)
        cart_product_form = CartAddProductForm()
        related_products = Product.objects.filter(category=p.category, active=True).exclude(pk=pk)[:4]
        return render(request, 'core/product_details.html', {'product': p, 'related_products': related_products, 'cart_product_form': cart_product_form})


class Products(View):
    def get(self, request):
        p = Product.objects.filter(active=True)
        count_product = Product.objects.all().count()
        paginator = Paginator(p, 9)
        page = request.GET.get("page")
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        return render(request, 'core/products.html', {"product": p, 'count': count_product})


class Category(View):
    def get(self, request, name):
        p = Product.objects.filter(category=name, active=True)
        paginator = Paginator(p, 9)
        page = request.GET.get("page")
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        return render(request, 'core/category.html', {'product': p})


class ShoppingCart(View):
    def get(self, request):
        return render(request, 'core/shopping_cart.html')

# ---------------- user profile ----------------


def user_profile(request):
    return render(request, 'core/user_profile.html')


# def update_profile(request, id):
#     if request.method == "POST":
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         phone = request.POST['phone']
#         address = request.POST['inputAddress']
#         city = request.POST['inputCity']
#         state = request.POST['inputAddress2']
#         zip_code = request.POST['inputZip']

        # image = request.FILES['image_file']
        # if (first_name == '' or last_name == '' or phone == '' or address == ''
        #         or city == '' or state == '' or zip_code == ''):
        #     messages.warning(request, "Please fill form Correctly..!")
        # else:
    #     user = CustomUser(first_name=first_name, last_name=last_name, phone=phone,
    #                       address=address, city=city, state=state, zip_code=zip_code, id=id)
    #     user.save()
    #     messages.success(request, "Data updated Successfully..!")
    # return redirect(user_profile)

# ---------------- user profile (end) ----------------

    # def post(self, request):
    #     if request.method == "POST":
    #         first_name = request.POST["first_name"]
    #         last_name = request.POST["last_name"]
    #         phone = request.POST["phone"]
    #         address = request.POST["inputAddress"]
    #         city = request.POST["inputCity"]
    #         state = request.POST["inputAddress2"]
    #         zip_code = request.POST["inputZip"]
    #
    #         user = CustomUser(first_name=first_name, last_name=last_name, phone=phone,
    #                           address=address, city=city, state=state, zip_code=zip_code)
    #         user.save()
    #     return render(request, 'core/user_profile.html')

# class DesktopNav(View):
#     def get(self, request):
#         user = CustomUser.objects.all()
#         return render(request, 'core/desktopNav.html', {'user': user})

class Signup(View):
    def get(self, request):
        return render(request, 'core/signup.html')

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)

        customer_group, created = Group.objects.get_or_create(name='Customer')

        # print(SignUpForm)
        # print(form.fields)
        # print(form.errors.as_json())
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            customer_group.user_set.add(user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('core/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'core/acc_active_sent.html')
        else:
            # form = SignUpForm()
            return render(request, 'core/signup.html', {'form': form})


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model()._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            # print(TypeError)
            # print(ValueError)
            # print(OverflowError)
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'core/acc_active_done.html')
        else:
            return render(request, 'core/acc_active_invalid.html')


def error404(request, exception):
    return render(request, 'core/404.html')


class Search(View):
    def get(self, request):
        q = request.GET.get('q')
        p = Product.objects.filter(name__icontains=q, active=True).order_by('-id')
        paginator = Paginator(p, 9)
        page = request.GET.get("page")
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        return render(request, 'core/search.html', {'product': p})


class OrderHistory(View):
    def get(self, request):
        orders = Order.objects.filter()
        return render(request, 'core/order_history.html', {'orders': orders})


class OrderDetails(View):
    def get(self, request):
        return render(request, 'core/order_details.html')


# ----------------for cart-----------------


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        print(cd)
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
        })
    return render(request, 'core/shopping_cart.html', {'cart': cart})

# ----------------for cart-----------------
