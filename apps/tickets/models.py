from django.db import models
from .choices import *

class Order(models.Model):
    order_id = models.IntegerField(unique=True)
    book_id = models.IntegerField()
    pnr_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    stamp_create = models.DateTimeField()

    def __str__(self):
        return f"Order {self.pnr_number}"
    
    class Meta:
        ordering = ['-stamp_create']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Passenger(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M', help_text="Пол пассажира")   
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='M', help_text="Тип пассажира")
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, help_text="Тип документа")
    document_number = models.CharField(max_length=100)
    document_expire = models.DateField()
    ticket_status = models.CharField(max_length=20,  help_text="Статус билета")
    price_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = 'Пассажир'
        verbose_name_plural = 'Пассажиры'
        

class FlightSegment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='segments')
    flight_number = models.CharField(max_length=20)
    departure_city = models.CharField(max_length=100)
    departure_airport = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.DateTimeField()
    arrival_city = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    arrival_date = models.DateField()
    arrival_time = models.DateTimeField()
    baggage = models.CharField(max_length=50)
    booking_class = models.CharField(max_length=10)
    duration = models.DurationField()
    duration_seconds = models.IntegerField()
    

    def __str__(self):
        return f"{self.departure_city} -> {self.arrival_city}"
    
    class Meta:
        verbose_name = 'Сегмент рейса'
        verbose_name_plural = 'Сегменты рейсов'
