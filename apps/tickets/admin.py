from django.contrib import admin
from .models import Order, Passenger, FlightSegment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'pnr_number', 'amount', 'currency', 'status', 'stamp_create')
    search_fields = ('pnr_number', 'order_id')
    list_filter = ('status', 'currency')
    ordering = ('-stamp_create',)
    date_hierarchy = 'stamp_create'
    inlines = []  


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date', 'gender', 'type', 'document_type', 'order')
    list_filter = ('gender', 'type', 'document_type')
    search_fields = ('last_name', 'first_name', 'document_number')
    raw_id_fields = ('order',)


@admin.register(FlightSegment)
class FlightSegmentAdmin(admin.ModelAdmin):
    list_display = (
        'flight_number', 'departure_city', 'arrival_city',
        'departure_date', 'arrival_date', 'booking_class',
        'duration', 'order'
    )
    search_fields = ('flight_number', 'departure_city', 'arrival_city')
    list_filter = ('departure_date', 'arrival_date', 'booking_class')
    raw_id_fields = ('order',)
