"""
Part 5: Real-World APIs - Enhanced Weather & Crypto Dashboard
=============================================================
Difficulty: Advanced

Features:
- Weather for multiple cities (Open-Meteo)
- Crypto prices and comparison (CoinPaprika)
- Top 5 cryptos by market cap
- Save results to JSON
- POST request example
- Optional API key support for OpenWeatherMap
"""

import requests
from datetime import datetime
import json
import os

# ======================
# City coordinates (latitude, longitude)
# ======================
CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "paris": (48.8566, 2.3522),
    "berlin": (52.5200, 13.4050)
}

# ======================
# Popular cryptocurrencies
# ======================
CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
    "ripple": "xrp-xrp"
}

# ======================
# Weather Functions
# ======================
def get_weather(city_name):
    """Fetch weather data using Open-Meteo API"""
    city_lower = city_name.lower().strip()
    if city_lower not in CITIES:
        print(f"\nCity '{city_name}' not found. Available cities: {', '.join(CITIES.keys())}")
        return None

    lat, lon = CITIES[city_lower]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None

def display_weather(city_name):
    """Display formatted weather information."""
    data = get_weather(city_name)
    if not data:
        return

    current = data["current_weather"]
    print(f"\n{'=' * 40}")
    print(f"  Weather in {city_name.title()}")
    print(f"{'=' * 40}")
    print(f"  Temperature: {current['temperature']}°C")
    print(f"  Wind Speed: {current['windspeed']} km/h")
    print(f"  Wind Direction: {current['winddirection']}°")
    
    weather_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        95: "Thunderstorm",
    }
    code = current.get("weathercode", 0)
    condition = weather_codes.get(code, "Unknown")
    print(f"  Condition: {condition}")
    print(f"{'=' * 40}")

# ======================
# Crypto Functions
# ======================
def get_crypto_price(coin_name):
    """Fetch crypto price"""
    coin_lower = coin_name.lower().strip()
    coin_id = CRYPTO_IDS.get(coin_lower, coin_lower)
    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching crypto data: {e}")
        return None

def display_crypto(coin_name):
    """Display crypto info"""
    data = get_crypto_price(coin_name)
    if not data:
        print(f"\nCoin '{coin_name}' not found. Available: {', '.join(CRYPTO_IDS.keys())}")
        return

    usd = data["quotes"]["USD"]
    print(f"\n{'=' * 40}")
    print(f"  {data['name']} ({data['symbol']})")
    print(f"{'=' * 40}")
    print(f"  Price: ${usd['price']:,.2f}")
    print(f"  Market Cap: ${usd['market_cap']:,.0f}")
    print(f"  24h Volume: ${usd['volume_24h']:,.0f}")
    print(f"  1h Change:  {usd['percent_change_1h']:+.2f}%")
    print(f"  24h Change: {usd['percent_change_24h']:+.2f}%")
    print(f"  7d Change:  {usd['percent_change_7d']:+.2f}%")
    print(f"{'=' * 40}")

def display_crypto_comparison(coins):
    """Compare multiple cryptos"""
    print(f"\n{'='*60}")
    print("  Cryptocurrency Comparison")
    print(f"{'='*60}")
    print(f"{'Name':<15}{'Price':>12}{'24h Change':>15}{'Market Cap':>20}")
    print(f"{'-'*60}")
    for coin in coins:
        data = get_crypto_price(coin)
        if not data:
            continue
        usd = data["quotes"]["USD"]
        print(f"{data['name']:<15}${usd['price']:>11,.2f}{usd['percent_change_24h']:>14.2f}%${usd['market_cap']:>19,.0f}")
    print(f"{'='*60}")

# ======================
# Top Cryptos
# ======================
def get_top_cryptos(limit=5):
    url = "https://api.coinpaprika.com/v1/tickers"
    params = {"limit": limit}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def display_top_cryptos():
    data = get_top_cryptos(5)
    if not data:
        return
    print(f"\n{'='*55}")
    print(f"  Top 5 Cryptocurrencies by Market Cap")
    print(f"{'='*55}")
    print(f"  {'Rank':<6}{'Name':<15}{'Price':<15}{'24h Change'}")
    print(f"  {'-'*50}")
    for coin in data:
        usd = coin["quotes"]["USD"]
        change = usd["percent_change_24h"]
        print(f"  {coin['rank']:<6}{coin['name']:<15}${usd['price']:>12,.2f}  {change:+.2f}%")
    print(f"{'='*55}")

# ======================
# POST Request Example
# ======================
def create_post_example():
    """Send a POST request to JSONPlaceholder"""
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {"title": "My Post", "body": "This is content", "userId": 1}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        print("\nPOST Request successful! Response:")
        print(json.dumps(data, indent=2))
        # Save to file
        with open("post_response.json", "w") as f:
            json.dump(data, f, indent=2)
    except requests.RequestException as e:
        print(f"Error creating post: {e}")

# ======================
# Save Results to JSON
# ======================
def save_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Results saved to {filename}")

# ======================
# Dashboard Menu
# ======================
def dashboard():
    print("\n" + "="*60)
    print("  Enhanced Weather & Crypto Dashboard")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    while True:
        print("\nOptions:")
        print("  1. Check Weather")
        print("  2. Check Crypto Price")
        print("  3. Compare Multiple Cryptos")
        print("  4. View Top 5 Cryptos")
        print("  5. Quick Dashboard (Delhi + Bitcoin)")
        print("  6. Create Sample POST Request")
        print("  7. Exit")

        choice = input("\nSelect (1-7): ").strip()

        if choice == "1":
            print(f"\nAvailable cities: {', '.join(CITIES.keys())}")
            city = input("Enter city name: ")
            display_weather(city)

        elif choice == "2":
            print(f"\nAvailable coins: {', '.join(CRYPTO_IDS.keys())}")
            coin = input("Enter crypto name: ")
            display_crypto(coin)

        elif choice == "3":
            coins = input("Enter crypto names (comma-separated): ").split(",")
            coins = [c.strip() for c in coins]
            display_crypto_comparison(coins)

        elif choice == "4":
            display_top_cryptos()

        elif choice == "5":
            display_weather("delhi")
            display_crypto("bitcoin")

        elif choice == "6":
            create_post_example()

        elif choice == "7":
            print("\nGoodbye! Happy coding!")
            break

        else:
            print("Invalid option. Try again.")

# ======================
# Run Dashboard
# ======================
if __name__ == "__main__":
    dashboard()







# --- CHALLENGE EXERCISES ---
#
# Exercise 1: Add more cities to the CITIES dictionary
#             Find coordinates at: https://www.latlong.net/
#
# Exercise 2: Create a function that compares prices of multiple cryptos
#             Display them in a formatted table
#
# Exercise 3: Add POST request example
#             Use: https://jsonplaceholder.typicode.com/posts
#             Send: requests.post(url, json={"title": "My Post", "body": "Content"})
#
# Exercise 4: Save results to a JSON file
#             import json
#             with open("results.json", "w") as f:
#                 json.dump(data, f, indent=2)
#
# Exercise 5: Add API key support for OpenWeatherMap
#             Sign up at: https://openweathermap.org/api
#             Use environment variables:
#             import os
#             api_key = os.environ.get("OPENWEATHER_API_KEY")
