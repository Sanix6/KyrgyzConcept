# from datetime import timedelta
# from django.utils.dateparse import parse_date, parse_datetime
# from apps.tickets.models import Order, Passenger, FlightSegment

# def parse_duration(duration_str):
#     if not duration_str:
#         return None
#     h, m, s = duration_str.split(':')
#     return timedelta(hours=int(h), minutes=int(m), seconds=int(s))


# def save_booking(response):
#     if response.get('status') != 1:
#         return None

#     data = response.get('data')
#     order = Order.objects.create(
#         order_id=data.get('order_id'),
#         book_id=data.get('book_id'),
#         pnr_number=data.get('pnr_number'),
#         amount=data.get('amount'),
#         currency=data.get('currency'),
#         status=data.get('status'),
#         stamp_create=data.get('stamp_create'),
#     )

#     passengers_to_create = []
#     for pax in data.get('passengers', []):
#         info = pax.get('info', {})
#         document = pax.get('document', {})
#         ticket = pax.get('ticket', {})
#         price = pax.get('price', {})

#         passengers_to_create.append(Passenger(
#             order=order,
#             first_name=info.get('firstname'),
#             last_name=info.get('lastname'),
#             birthdate=info.get('birthdate'),
#             gender=info.get('gender'),
#             type=info.get('type'),
#             document_number=document.get('number'),
#             document_expire=document.get('expire'),
#             ticket_status=ticket.get('status'),
#             price_total=price.get('total'),
#         ))
#     if passengers_to_create:
#         Passenger.objects.bulk_create(passengers_to_create)

#     segments_data = data.get('segments', {})
#     segments_to_create = []

#     for seg in segments_data.values():
#         dep = seg.get('departure', {})
#         arr = seg.get('arrival', {})

#         departure_date = parse_date(dep.get('date'))
#         arrival_date = parse_date(arr.get('date'))

#         departure_time_str = f"{dep.get('date')} {dep.get('time')}"
#         arrival_time_str = f"{arr.get('date')} {arr.get('time')}"

#         departure_time = parse_datetime(departure_time_str)
#         arrival_time = parse_datetime(arrival_time_str)

#         segments_to_create.append(FlightSegment(
#             order=order,
#             flight_number=seg.get('flight_number', ''),
#             departure_city=dep.get('city', {}).get('name', ''),
#             departure_airport=dep.get('airport', {}).get('name', ''),
#             departure_date=departure_date,
#             departure_time=departure_time,
#             arrival_city=arr.get('city', {}).get('name', ''),
#             arrival_airport=arr.get('airport', {}).get('name', ''),
#             arrival_date=arrival_date,
#             arrival_time=arrival_time,
#             baggage=seg.get('baggage', ''),
#             booking_class=seg.get('booking_class', ''),
#             duration=parse_duration(seg.get('duration')),
#             duration_seconds=seg.get('duration_seconds', 0)
#         ))

#     if segments_to_create:
#         FlightSegment.objects.bulk_create(segments_to_create)

#     return order  
