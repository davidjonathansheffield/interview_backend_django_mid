from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'language', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'language', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'type__name', 'language__name')
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'language', 'tags', 'metadata', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')