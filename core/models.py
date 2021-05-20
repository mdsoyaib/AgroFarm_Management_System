# from django.forms import forms, ModelForm, EmailField, TextInput
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class InhouseProduct(models.Model):
    category = (
        ("Fertilizer", 'FERTILIZER'),
        ("Seed", "SEED")
    )
    unit_type = (
        ("KILOGRAM", "Kilogram"),
        ("LITER", "Liter"),
        ("PIECE", "Piece"),
        ("CUSTOM", "Custom"),
    )

    name = models.CharField(max_length=50)
    details = models.TextField(null=True, blank=True)
    price_per_unit = models.PositiveIntegerField(null=True, blank=True)
    category = models.CharField(
        max_length=50,
        choices=category,
    )
    unit_type = models.CharField(
        max_length=20,
        choices=unit_type,
    )
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)

    def __str__(self):
        return f"{self.name}"


class InhouseStock(models.Model):
    inhouse_product = models.OneToOneField(InhouseProduct, on_delete=models.CASCADE)
    stock_in = models.PositiveIntegerField()
    stock_out = models.PositiveIntegerField(null=True, blank=True)
    current_stock = models.PositiveIntegerField(null=True, blank=True, editable=True)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


# @receiver(pre_save, sender=InhouseStock)
# def abcd(sender, **kwargs):
#     stock = kwargs['instance']
#     out = InhouseStock.objects.get(id=stock.stock_out)
#     stock.current_stock = stock.stock_in - out.stock_out
#     stock.save()

    # def updated_stock(self):
    #         self.current_stock = 10
    #         return self.current_stock


class Instrument(models.Model):
    name = models.CharField(max_length=50, unique=True)
    details = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


class Worker(models.Model):
    gender = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("CUSTOM", "Custom"),
    )

    name = models.CharField(max_length=100, help_text="Enter name (required)")
    phone_number1 = models.CharField(unique=True, max_length=14)
    phone_number2 = models.CharField(null=True, blank=True, unique=True, max_length=14)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        help_text="Select gender",
        choices=gender,
    )
    task = models.CharField(max_length=50, null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


# class ExpenseType(models.Model):
#     exp_name = models.CharField(max_length=50)
#     status = models.BooleanField(max_length=10)


class Expenses(models.Model):
    # expenseType_id = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    exp_type = (
        ("ELECTRICITY BILL", 'Electricity Bill'),
        ("LAND BILL", "Land Bill"),
        ("WORKER SALARY", "Worker Salary"),
        ("INSTRUMENT", "Instrument"),
        ("SEED", "Seed"),
        ("FERTILIZER", "Fertilizer"),
        ("OTHERS", "Others")
    )

    status = (
        ("PAID", 'Paid'),
        ("NON-PAID", "Non-Paid")
    )

    exp_type = models.CharField(
        max_length=50,
        choices=exp_type,
    )
    exp_name = models.CharField(max_length=50)
    details = models.TextField(null=True, blank=True)
    amount = models.PositiveIntegerField()
    month = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=status,
    )
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


class Product(models.Model):
    unit_type = (
        ("KILOGRAM", "Kilogram"),
        ("LITER", "Liter"),
        ("PIECE", "Piece"),
        ("CUSTOM", "Custom"),
    )
    category = (
        ("FRUIT", "Fruit"),
        ("VEGETABLE", "Vegetable"),
        ("LIQUID", "Liquid"),
        ("DAIRY", "Dairy"),
        ("GROCERY", "Grocery"),
    )
    name = models.CharField(max_length=100, unique=True)
    details = models.TextField(null=True, blank=True)
    price_per_unit = models.PositiveIntegerField()
    unit_type = models.CharField(
        max_length=20,
        choices=unit_type,
    )
    category = models.CharField(
        max_length=50,
        choices=category,
    )
    product_image = models.ImageField(null=True, blank=True, default='/core/images/default.png', upload_to='core/images')
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)

    def __str__(self):
        return f"{self.name}"


class ProductStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_in = models.PositiveIntegerField()
    stock_out = models.PositiveIntegerField(null=True, blank=True)
    current_stock = models.PositiveIntegerField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


# class BuyerForm(ModelForm):
#     email_id = EmailField(
#         required=False,
#         widget=TextInput(
#             attrs={'placeholder':'please enter your email',}
#         )
#     )
#
#     class Meta:
#         model = Buyer
#         fields = ['email_id',]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("user must have an email address")

        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, default=None, null=True)
    last_name = models.CharField(max_length=255, default=None, null=True)

    email = models.EmailField(max_length=100, unique=True)

    username = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    session_token = models.CharField(max_length=10, default=0)

    is_active = models.BooleanField(default=False)
    # a admin user; non super-user
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # a superuser

    phone = models.CharField(max_length=255, default=None, null=True, blank=True)
    address = models.TextField(default=None, null=True, blank=True)
    city = models.CharField(max_length=255, default=None, null=True, blank=True)
    state = models.CharField(max_length=255, default=None, null=True, blank=True)
    zip_code = models.CharField(max_length=255, default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    profile_image = models.FileField(upload_to='core/user')

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


class Order(models.Model):
    status = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("CANCELED", "Canceled"),
        ("DELIVERED", "Delivered"),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='Pending', choices=status)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)


class WebsiteInfo(models.Model):
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    open_time = models.CharField(max_length=255)
    email = models.EmailField()

    map_city = models.CharField(max_length=255)
    map_phone = models.CharField(max_length=255)
    map_address = models.CharField(max_length=255)

    about_us = models.TextField()
    contact_info = models.TextField()
    payment_method = models.TextField()

    active = models.BooleanField(default=True)



