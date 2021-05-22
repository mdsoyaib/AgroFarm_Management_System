# import form as form
from django.contrib import admin
from core.models import InhouseProduct, Instrument, Worker, Expenses, \
    Product, ProductStock, Order, OrderDetail, CustomUser, WebsiteInfo, InhouseStock

# Register your models here.

admin.site.site_title = "AgroFarm"
admin.site.site_header = "AgroFarm Admin Panel"

admin.site.register(CustomUser)


@admin.register(InhouseProduct)
class InhouseProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'details', 'category', 'price_per_unit', 'unit_type')
    list_filter = ('category', 'unit_type')
    search_fields = ('name', 'category', 'unit_type')
    list_per_page = 20


@admin.register(InhouseStock)
class InhouseStockAdmin(admin.ModelAdmin):
    list_display = ('inhouse_product', 'stock_in', 'stock_out', 'current_stock')
    # list_editable = ('stock_in', 'stock_out', 'current_stock')
    search_fields = ('inhouse_product',)
    readonly_fields = ('current_stock',)
    list_per_page = 20


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'details', 'quantity', 'price_per_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number1', 'phone_number2', 'address', 'gender', 'task', 'salary')
    list_filter = ('gender', 'task', 'salary')
    search_fields = ('phone_number1', 'name', 'phone_number2')
    list_per_page = 20


# @admin.register(ExpenseType)
# class ExpenseTypeAdmin(admin.ModelAdmin):
#     list_display = ('exp_name', 'status')
#     list_filter = ('exp_name', 'status')


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('exp_type', 'exp_name', 'details', 'amount', 'month', 'status')
    list_filter = ('exp_type', 'month', 'status')
    search_fields = ('exp_type', 'exp_name', 'month', 'status')
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_unit', 'unit_type', 'category', 'product_image', 'active', 'featured')
    list_filter = ('unit_type', 'category', 'active', 'featured')
    search_fields = ('name', 'category', 'unit_type')
    list_per_page = 20
    # ordering = ('name',)


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock_in', 'stock_out', 'current_stock')
    list_editable = ('stock_in',)
    search_fields = ('product',)
    readonly_fields = ('stock_out', 'current_stock',)
    list_per_page = 20


# @admin.register(Buyer)
# class BuyerAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email_id', 'phone_number1', 'phone_number2',
#                     'address', 'gender', 'password')
#     list_filter = ('first_name', 'gender')
#     search_fields = ('first_name', 'last_name', 'email_id', 'phone_number1', 'phone_number2',
#                      'gender')
#     list_per_page = 20

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     kwargs['widgets'] = {
    #         'email_id': form.TextField()
    #     }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'order_time', 'total_price', 'status')
    search_fields = ('customer', 'order_date', 'order_time', 'status')
    list_filter = ('status',)
    # readonly_fields = ('buyer', 'order_date', 'order_time')
    list_per_page = 20


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')
    # readonly_fields = ('order', 'product', 'quantity', 'price')
    list_per_page = 20


@admin.register(WebsiteInfo)
class WebsiteInfoAdmin(admin.ModelAdmin):
    list_display = ('active', 'phone', 'address', 'open_time', 'email', 'map_city', 'map_phone',
                    'map_address', 'contact_info', 'payment_method')
    list_display_links = ('phone',)
    list_filter = ('active',)


# @admin.register(Salary)
# class SalaryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'salary', 'bonus', 'total_salary')