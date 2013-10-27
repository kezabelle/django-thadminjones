# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TestModelFields, ReducedPermissions
from thadminjones.admin import SupportsQuickAdd


class TestModelAdmin(SupportsQuickAdd, admin.ModelAdmin):
    pass
admin.site.register(TestModelFields, TestModelAdmin)


class TestReducedPermissions(SupportsQuickAdd, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(ReducedPermissions, TestReducedPermissions)
