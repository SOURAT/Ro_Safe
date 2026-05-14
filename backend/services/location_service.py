import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="drivelegal-ai", timeout=10)


def get_location_details(lat, lon, retries=2):
    try:
        lat = float(lat)
        lon = float(lon)

        for _ in range(retries):
            try:
                location = geolocator.reverse((lat, lon), language="en")

                if not location:
                    return {"error": "Location not found"}

                address = location.raw.get("address", {})

                state = address.get("state")
                district = address.get("state_district") or address.get("county")
                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("village")
                    or district
                )
                road = (
                    address.get("road")
                    or address.get("neighbourhood")
                    or address.get("suburb")
                )
                country = address.get("country")          # added
                country_code = address.get("country_code") # added

                return {
                    "state": state,
                    "district": district,
                    "city": city,
                    "road": road,
                    "country": country,                    # added
                    "country_code": country_code.upper() if country_code else None  # added
                }

            except GeocoderTimedOut:
                time.sleep(1)

        return {"error": "Geocoder timeout"}

    except (ValueError, TypeError):
        return {"error": "Invalid coordinates"}

    except GeocoderServiceError as e:
        return {"error": f"Service error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
