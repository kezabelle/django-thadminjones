# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TestModelFields, ReducedPermissions, TestInlineModel
from thadminjones.admin import SupportsQuickAdd


class TestStackedInline(admin.StackedInline):
    model = TestInlineModel
    extra = 1


class TestTabularInline(admin.TabularInline):
    model = TestInlineModel
    extra = 1
    max_num = 2


class TestModelAdmin(SupportsQuickAdd, admin.ModelAdmin):
    inlines = [
        TestStackedInline,
        TestTabularInline,
    ]
    fieldsets = [
        (None, {'fields': [
            'big_int',
            'yesno',
            ('title', 'csv_data'),
            ('when', 'when_accurate'),
            ('amount', 'email'),
            'upload', 'path', 'inaccurate',
        ]}),
        ("More fields", {'fields': [
            'img',
            'ip',
            'better_ip',
            ('yesnomaybe', 'posint', 'small_posint'),
            'slug',
            'small_int',
            'content',
            'when_time',
            'web_address',
            'user',
            'groups',
            'one_to_one']
        })
    ]
admin.site.register(TestModelFields, TestModelAdmin)


class TestReducedPermissions(SupportsQuickAdd, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(ReducedPermissions, TestReducedPermissions)
