"""
Part 1: Basic GET Request
=========================
Difficulty: Beginner

Learn: How to make simple GET requests and view the response.

We'll use JSONPlaceholder - a free fake API for testing.
"""

import requests

# ----------------------------
# Step 1: Basic GET request
# ----------------------------
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print("=== Basic API Request ===\n")
print(f"URL: {url}")
print(f"Status Code: {response.status_code}")
print(f"Response Data:\n{response.json()}")
print("\n" + "="*50 + "\n")

# ----------------------------
# Exercise 1: Fetch post number 5
# ----------------------------
url_post5 = "https://jsonplaceholder.typicode.com/posts/5"
response_post5 = requests.get(url_post5)

print("=== Exercise 1: Post #5 ===\n")
print(f"URL: {url_post5}")
print(f"Status Code: {response_post5.status_code}")
print(f"Response Data:\n{response_post5.json()}")
print("\n" + "="*50 + "\n")

# ----------------------------
# Exercise 2: Fetch all users
# ----------------------------
url_users = "https://jsonplaceholder.typicode.com/users"
response_users = requests.get(url_users)

print("=== Exercise 2: All Users ===\n")
print(f"URL: {url_users}")
print(f"Status Code: {response_users.status_code}")
print(f"Number of users fetched: {len(response_users.json())}")
print(f"First User:\n{response_users.json()[0]}")  # print first user as example
print("\n" + "="*50 + "\n")

# ----------------------------
# Exercise 3: Fetch a post that doesn't exist
# ----------------------------
url_nonexistent = "https://jsonplaceholder.typicode.com/posts/999"
response_nonexistent = requests.get(url_nonexistent)

print("=== Exercise 3: Nonexistent Post ===\n")
print(f"URL: {url_nonexistent}")
print(f"Status Code: {response_nonexistent.status_code}")
# JSONPlaceholder returns {} if post does not exist
print(f"Response Data:\n{response_nonexistent.json()}")
