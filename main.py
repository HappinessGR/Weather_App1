import requests
from datetime import datetime

API_KEY = "b2a5adcct04b33178913oc335f405433"

def get_weather(city: str) -> None:
    city = city.strip()
    if not city:
        print("Please enter a city name.")
        return

    url = f"https://api.shecodes.io/weather/v1/current?query={city}&key={API_KEY}&units=metric"

    try:
        resp = requests.get(url, timeout=10)

        if resp.status_code == 404:
            print(f"City '{city}' not found. Please try another name.")
            return
        if resp.status_code != 200:
            print(f"Error: Could not fetch weather data for '{city}' (status {resp.status_code}).")
            return

        try:
            data = resp.json()
        except ValueError:
            print(f"Error: Unexpected (non-JSON) response from the API for '{city}'.")
            return

        if isinstance(data, dict) and ("error" in data or "message" in data):
            print(f"Error: {data.get('error') or data.get('message')}")
            return

        if not isinstance(data, dict) or "temperature" not in data or "city" not in data:
            print(f"Error: Unexpected API response format for '{city}'.")
            return

        temperature = round(data["temperature"]["current"])
        city_name = data["city"]
        description = data.get("condition", {}).get("description", "N/A")
        icon_url = data.get("condition", {}).get("icon_url", "")

        now = datetime.now()
        formatted_date = now.strftime("%A %H:%M")

        print("\n===============================")
        print(f"Weather in {city_name}")
        print(f"Date & Time : {formatted_date}")
        print(f"Temperature : {temperature}°C")
        print(f"Condition   : {description.capitalize() if isinstance(description, str) else 'N/A'}")
        if icon_url:
            print(f"Icon URL    : {icon_url}")
        print("===============================\n")

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Network problem ({e.__class__.__name__}). Please check your connection and try again.")

if __name__ == "__main__":
    while True:
        city = input("Enter a city (or type 'exit' to quit): ")
        if city.lower().strip() == "exit":
            print("Exiting the program. Goodbye!")
            break
        get_weather(city)
