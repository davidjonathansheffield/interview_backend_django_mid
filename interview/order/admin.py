from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory', 'start_date', 'embargo_date', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'start_date', 'embargo_date', 'created_at', 'updated_at')
    search_fields = ('inventory__name',)
    filter_horizontal = ('tags',)
    date_hierarchy = 'start_date'

    fieldsets = (
        (None, {
            'fields': ('inventory', 'start_date', 'embargo_date', 'tags', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')