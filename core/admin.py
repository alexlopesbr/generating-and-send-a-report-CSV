from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Seller, Product, ProductSold, Client
# from rest_framework.authtoken.models import Token

admin.site.site_header = 'System Payment Admin'


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email',
                           'password',
                           'name',
                           'birthday',
                           'cpf',
                           'verified_phone',
                           'phone',
                           'username',
                           'profile_image',

                           'is_active')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.unregister(DjangoGroup)
admin.site.register(User, UserAdmin)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(ProductSold)
admin.site.register(Client)
