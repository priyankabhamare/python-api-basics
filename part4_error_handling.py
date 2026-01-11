"""
Part 4: Robust Error Handling
=============================
Difficulty: Intermediate+

Learn:
- Try/except blocks for API requests
- Handling network errors
- Timeout handling
- Response validation
- Retry logic
- Logging API requests
"""

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
import time
import logging

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def safe_api_request(url, timeout=5, retries=3):
    """
    Make an API request with proper error handling and retry logic.
    
    Parameters:
        url (str): API endpoint
        timeout (int): seconds before timeout
        retries (int): number of retry attempts
    Returns:
        dict: {"success": True, "data": response.json()} or {"success": False, "error": msg}
    """
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Attempt {attempt}: GET {url}")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return {"success": True, "data": response.json()}

        except (ConnectionError, Timeout, HTTPError, RequestException) as e:
            logging.warning(f"Attempt {attempt} failed: {str(e)}")
            if attempt < retries:
                logging.info("Retrying...")
                time.sleep(1)
            else:
                return {"success": False, "error": str(e)}

    return {"success": False, "error": "Unknown error"}


# --- Demo Error Handling ---
def demo_error_handling():
    print("=== Error Handling Demo ===\n")

    # Test 1: Successful request
    print("--- Test 1: Valid URL ---")
    result = safe_api_request("https://jsonplaceholder.typicode.com/posts/1")
    if result["success"]:
        print(f"Success! Got post: {result['data']['title'][:30]}...")
    else:
        print(f"Failed: {result['error']}")

    # Test 2: 404 Error
    print("\n--- Test 2: Non-existent Resource (404) ---")
    result = safe_api_request("https://jsonplaceholder.typicode.com/posts/99999")
    if result["success"]:
        print(f"Success! Data: {result['data']}")
    else:
        print(f"Failed: {result['error']}")

    # Test 3: Invalid domain
    print("\n--- Test 3: Invalid Domain ---")
    result = safe_api_request("https://this-domain-does-not-exist-12345.com/api")
    if result["success"]:
        print(f"Success!")
    else:
        print(f"Failed: {result['error']}")

    # Test 4: Timeout simulation
    print("\n--- Test 4: Timeout Simulation ---")
    result = safe_api_request("https://httpstat.us/200?sleep=5000", timeout=1)
    if result["success"]:
        print(f"Success!")
    else:
        print(f"Failed: {result['error']}")


# --- Validate JSON Response ---
def validate_json_response():
    print("\n=== JSON Validation Demo ===\n")

    url = "https://jsonplaceholder.typicode.com/users/1"

    result = safe_api_request(url)
    if result["success"]:
        data = result["data"]
        required_fields = ["name", "email", "phone"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            print(f"Warning: Missing fields: {missing}")
        else:
            print("All required fields present!")
            print(f"Name: {data['name']}")
            print(f"Email: {data['email']}")
            print(f"Phone: {data['phone']}")
    else:
        print(f"Error fetching data: {result['error']}")


# --- Safe Crypto Price Checker with Validation ---
def fetch_crypto_safely():
    print("\n=== Safe Crypto Price Checker ===\n")

    coin = input("Enter coin (btc-bitcoin, eth-ethereum): ").strip().lower()
    if not coin:
        print("Error: Please enter a coin name.")
        return

    url = f"https://api.coinpaprika.com/v1/tickers/{coin}"
    result = safe_api_request(url)

    if result["success"]:
        data = result["data"]
        # Validate response keys
        if "quotes" in data and "USD" in data["quotes"]:
            price_usd = data["quotes"]["USD"]["price"]
            change_24h = data["quotes"]["USD"]["percent_change_24h"]
            print(f"\n{data['name']} ({data['symbol']})")
            print(f"Price: ${price_usd:,.2f}")
            print(f"24h Change: {change_24h:+.2f}%")
        else:
            print("Error: Unexpected response structure. Missing 'quotes' or 'USD' key.")
    else:
        print(f"\nError: {result['error']}")
        print("Tip: Try 'btc-bitcoin' or 'eth-ethereum'")


# --- Main Program ---
def main():
    demo_error_handling()
    print("\n" + "=" * 40 + "\n")
    validate_json_response()
    print("\n" + "=" * 40 + "\n")
    fetch_crypto_safely()


if __name__ == "__main__":
    main()
