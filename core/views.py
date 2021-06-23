import os

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
from core.models import Product, WebsiteInfo, CustomUser, Order, TestOrder, OrderDetail, BillingInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .cart import Cart
from .forms import CartAddProductForm
from django.conf import settings
from .pdf import pdf_creator
from django.db.models import F


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
    # print(request.session['cart'])
    # print(len(cart))
    # if len(cart) > 0:
    #
    #     return render(request, 'core/checkout.html', {'cart': cart})
    # else:
    #     messages.warning(request, "Sorry! Your cart is empty..!")
    return render(request, 'core/checkout.html', {'cart': cart})


def insert_order(request):
    cart = Cart(request)
    if request.method == "POST":
        total_price = request.POST["total_price"]
        user = request.user
        # print(request.POST)
        # print(request.session['cart'])
        # checkcart = request.session['cart']
        # if checkcart == {}:
        #     return redirect()
        if (total_price == '0'):
            messages.warning(request, "Sorry! Your cart is empty..!")
        else:
            order = Order(total_price=total_price, customer=user)
            order.save()
            cart.clear()
            # print(order.id)

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address=request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            phone = request.POST['phone']

            billing = BillingInfo(first_name=first_name, last_name=last_name, address=address, city=city,
                                  state=state, zip_code=zip_code, phone=phone, order=order, customer=user)
            billing.save()

            for item in cart:
                product = item['product']
                quantity = item['quantity']
                price = item['total_price']
                order_details = OrderDetail(quantity=quantity, price=price, product=product, order=order)
                order_details.save()
                # find product by id
                # print(item)
                Product.objects.filter(id=item['id']).update(quantity=F('quantity')-item['quantity'])
                # update product qauntity old_qyt - cartqyt

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


def update_profile(request, id):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        address = request.POST['inputAddress']
        city = request.POST['inputCity']
        state = request.POST['inputAddress2']
        zip_code = request.POST['inputZip']

        if (first_name == '' or last_name == '' or phone == '' or address == ''
                or city == '' or state == '' or zip_code == ''):
            messages.warning(request, "Please fill form Correctly..!")
        else:
            user = CustomUser(first_name=first_name, last_name=last_name, phone=phone,
                              address=address, city=city, state=state, zip_code=zip_code, id=id)
            user.save()
            messages.success(request, "Data updated Successfully..!")
    return redirect(user_profile)

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

# ------------ for Order History -----------------


class OrderHistory(View):
    def get(self, request):
        orders = Order.objects.filter().order_by('-id')
        return render(request, 'core/order_history.html', {'orders': orders})


class OrderDetails(View):
    def get(self, request, pk):
        product = Product.objects.all()
        orders = Order.objects.get(pk=pk)
        history = OrderDetail.objects.all()
        return render(request, 'core/order_details.html', {'history': history, 'orders': orders, 'product': product})

# ------------ for Order History -----------------


class OrderReport(View):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        # pdfcreator
        # if request.method == "POST":
        #     from_date = request.POST.get("from_date")
        #     to_date = request.POST.get("to_date")
        #     search = Order.objects.raw('select pk, customer, order_date, order_time, status from order where order_date between "'+from_date+'" and "'+to_date+'"')
        #     return render(request, 'core/order_report.html', {'orders': search})
        # else:

        # if request.method=="POST":
        #     from_date = request.POST['from_date']
        #     to_date = request.POST['to_date']
        #     try:
        #         date = Order.objects.filter(order_date__lte=from_date, order_date__gte=to_date)
        #     except:
        #         date=None
        #     return render(request, 'core/order_report.html', {'date': date})

        paginator = Paginator(orders, 12)
        page = request.GET.get("page")
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        return render(request, 'core/order_report.html', {'orders': orders})


# import io
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
#
# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return

def PdfOrderReport(request, pk):
    product = Product.objects.all()
    orders = Order.objects.get(pk=pk)
    history = OrderDetail.objects.all()
    billing = BillingInfo.objects.all()
    # pdf_creator()

    # dict = {
    #     'first_name': orders.customer.first_name,
    #     'last_name': orders.customer.last_name,
    #     'email': orders.customer.email,
    #     'phone': orders.customer.phone,
    #     'product': history.product,
    #     'quantity': history.quantity,
    #     'price_per_unit': history.product.price_per_unit,
    #     'price': history.price,
    #     'pk': orders.pk,
    #     'order_date': orders.order_date,
    #     'order_time': orders.order_time,
    #     'total_price': orders.total_price,
    # }
    # return render_to_pdf('core/pdf_order_report.html', dict)
    return render(request, 'core/pdf_order_report.html', {'history': history, 'orders': orders, 'product': product, 'billing': billing})


def create_pdf(request):
    host = 'http://' + settings.ALLOWED_HOSTS[0] + ':8000'
    partial_url = request.POST.get('url', '')
    output = partial_url.split('/')[-1]
    url = host + partial_url
    pdf_creator(url, output)
    # return HttpResponse(url)
    # return redirect(url)

    file_path = os.path.join(settings.BASE_DIR, output + '.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


class UserInfo(View):
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        orders = Order.objects.all().order_by('-id')
        return render(request, 'core/user_info.html', {'user': user, 'orders': orders})

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


def payment(request):
    return render(request, 'core/payment.html')