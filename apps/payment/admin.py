from django.contrib import admin
from .models import MkassaPayment

@admin.register(MkassaPayment)
class MkassaPaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'amount', 'status', 'created_at', 'updated_at']
    search_fields = ['payment_id', 'user__phone', 'user__email', 'status']
    list_filter = ['status', 'created_at']
