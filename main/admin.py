from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.translation import gettext as _
from main import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]
    list_filter = ("updated_at",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name", "image", "location")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important_dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password", "password2")}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.ItemImageModel)
admin.site.register(models.ItemModel, OSMGeoAdmin)
admin.site.register(models.Category)
admin.site.register(models.Message)
admin.site.unregister(Group)


admin.site.site_header = "Share it admin page"
admin.site.site_title = "Share it admin area"
admin.site.index_title = "Share it administration"
