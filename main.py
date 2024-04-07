from pprint import pprint
import requests
import os
from datetime import datetime,timedelta
from flight_search import FlightSearch
from data_manager import  DataManager
from notification_manager import NotificationManager

data_manager=DataManager()
sheet_data=data_manager.get_destination_data()
flight_search=FlightSearch()
notification_manager=NotificationManager()


if sheet_data[0]['iataCode']=='':
    flight_search=FlightSearch()
    for row in sheet_data:
        row['iataCode']=flight_search.get_destination_code(row['city'])
        # row['iataCode']=''

    data_manager.destination_data=sheet_data
    data_manager.update_destination_codes()

ORIGIN_CITY_IATA='DFW'
tomorrow=datetime.now()+timedelta(days=1)
six_month_from_today=datetime.now()+timedelta(days=180)

for destination in sheet_data:
    flight=flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination['iataCode'],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight:
        if flight.price<destination['lowestPrice']:
            notification_manager.send_email(message=f"Low price alert! Only ${flight.price} to fly from"
                                                    f"{flight.origin_city}-{flight.origin_airport} to "
                                                    f"{flight.destination_city}-{flight.destination_airport}"
                                                    f"from {flight.out_date} to {flight.return_date}")
