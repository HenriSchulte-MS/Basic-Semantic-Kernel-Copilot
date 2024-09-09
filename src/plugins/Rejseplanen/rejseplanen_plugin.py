from typing import Annotated, Optional
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import requests

class RejseplanenPlugin:

    endpoint = "http://xmlopen.rejseplanen.dk/bin/rest.exe/"

    @kernel_function(
        description="Get the location ID for a station name",
        name="getLocationId"
    )
    def get_location_id(self, station_name: Annotated[str, "The name of a city or station"]) -> Annotated[str, "The ID of the location"]:
        url = f"{self.endpoint}location?input={station_name}&format=json"
        response = requests.get(url)
        return response.json()
    
    
    @kernel_function(
    description="Get next 5 public transport departures from a station ID",
    name="getDepartures"
    )
    def get_departures(
        self,
        id: Annotated[str, "ID of the location"],
        time: Annotated[Optional[str], "Time of departure in HH:MM 24h format"] = "",
        date: Annotated[Optional[str], "Date of departure as DD.MM.YYYY"] = ""
    ) -> Annotated[str, "A list of departures"]:
        
        url = f"{self.endpoint}departureBoard?id={id}&date={date}&time={time}&format=json"
        response = requests.get(url)
        response_json = response.json()
        return response_json['DepartureBoard']['Departure'][:5] # Return the first 5 departures