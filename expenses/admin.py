from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'category', 'amount', 'description')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description',)
    date_hierarchy = 'date'
