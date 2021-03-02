from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from . import models


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_stock', 'price')
    list_filter = ('active', 'in_stock', 'date_updated',)
    list_editable = ('in_stock',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('tags',)


admin.site.register(models.Product, ProductAdmin)


class ProductTag(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# autocomplete_fields = ('tags',)


admin.site.register(models.ProductTag, ProductTag)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name')
    readonly_fields = ('thumbnail',)
    search_fields = ('product_name',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="/%s"/>' % obj.thumbnail.url)
        return '-'

    thumbnail_tag.short_description = 'Thumbnail'

    def product_name(self, obj):
        return obj.product.name


admin.site.register(models.ProductImage, ProductImageAdmin)


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal Info',
            {'fields': ('first_name', 'last_name')},
        ),
        (
            'permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'group',
                    'user_permissions'
                )
            },
        ),
        (
            'Important dates',
            {'fields': ('last_login', 'date_joined')},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            }
        ),
    )
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class BasketLineInline(admin.TabularInline):
    model = models.BasketLine
    raw_id_fields = ('product',)


@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'count')
    list_editable = ('status',)
    list_filter = ('status',)
    inlines = (BasketLineInline,)


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    raw_id_fields = ('product',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')
    list_editable = ('status',)
    list_filter = ('status', 'shipping_country', 'date_added')
    inlines = (OrderLineInline,)
    fieldsets = (
        ('User Info', {'fields': ('user', 'status')}),
        (
            'Billing info',
            {
                'fields': (
                    'billing_name',
                    'billing_address1',
                    'billing_address2',
                    'billing_zip_code',
                    'billing_city',
                    'billing_country',
                )
            },
        ),
        (
            'Shipping Info',
            {
                'fields': (
                    'shipping_name',
                    'shipping_address1',
                    'shipping_address2',
                    'shipping_zip_code',
                    'shipping_city',
                    'shipping_country',
                )
            },
        ),
    )
