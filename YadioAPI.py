##################
# Yadio API v1.0 #
# By AlerrandroV #
##################

import requests
import pytz
from datetime import datetime, timedelta

# Base URL for the Yadio API
YADIO_API_URL = 'https://api.yadio.io'

def response(url: str) -> dict:
	"""
	Makes a GET request to the specified URL and returns the JSON response.

	Args:
		url (str): The URL to make the request to.

	Returns:
		dict: The JSON response from the API, or None if an error occurs.
	"""
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.HTTPError as e:
		print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
	except requests.exceptions.RequestException as e:
		print(f"Request Error: {e}")
	return None

def exrates(currency: str) -> dict:
	"""
	Fetches the exchange rates for the specified currency.

	Args:
		currency (str): The currency code (e.g., 'BTC', 'USD').

	Returns:
		dict: The exchange rates for the specified currency.
	"""
	currency = currency.upper()
	url = f'{YADIO_API_URL}/exrates/{currency}'
	return response(url)

def convert(amount: float, input_currency: str, output_currency: str) -> dict:
	"""
	Converts an amount from one currency to another using the Yadio API.

	Args:
		amount (float): The amount to convert.
		input_currency (str): The source currency code (e.g., 'BTC').
		output_currency (str): The target currency code (e.g., 'USD').

	Returns:
		dict: The conversion result from the API.
	"""
	try:
		amount = float(amount)
	except ValueError:
		raise ValueError("The 'amount' parameter must be a number.")

	input_currency = input_currency.upper()
	output_currency = output_currency.upper()
	url = f'{YADIO_API_URL}/convert/{amount}/{input_currency}/{output_currency}'
	return response(url)

def rate(input_currency: str, output_currency: str) -> dict:
	"""
	Fetches the exchange rate between two currencies.

	Args:
		input_currency (str): The source currency code (e.g., 'BTC').
		output_currency (str): The target currency code (e.g., 'USD').

	Returns:
		dict: The exchange rate between the two currencies.
	"""
	input_currency = input_currency.upper()
	output_currency = output_currency.upper()
	url = f'{YADIO_API_URL}/rate/{input_currency}/{output_currency}'
	return response(url)

def currencies() -> dict:
	"""
	Fetches the list of supported currencies.

	Returns:
		dict: A list of supported currencies.
	"""
	url = f'{YADIO_API_URL}/currencies'
	return response(url)

def exchanges() -> dict:
	"""
	Fetches the list of supported exchanges.

	Returns:
		dict: A list of supported exchanges.
	"""
	url = f'{YADIO_API_URL}/exchanges'
	return response(url)

def today(time_range: float, currency: str) -> dict:
	"""
	Fetches the exchange rates for the specified currency over a time range.

	Args:
		time_range (float): The time range in hours.
		currency (str): The currency code (e.g., 'BTC').

	Returns:
		dict: The exchange rates for the specified time range.
	"""
	currency = currency.upper()
	url = f'{YADIO_API_URL}/today/{float(time_range)}/{currency}'
	return response(url)

def hist(time_range: float, currency: str) -> dict:
	"""
	Fetches historical exchange rates for the specified currency over a time range.

	Args:
		time_range (float): The time range in days.
		currency (str): The currency code (e.g., 'BTC').

	Returns:
		dict: The historical exchange rates.
	"""
	currency = currency.upper()
	url = f'{YADIO_API_URL}/hist/{float(time_range)}/{currency}'
	return response(url)

def compare(time_range: float, currency: str) -> dict:
	"""
	Compares exchange rates for the specified currency over a time range.

	Args:
		time_range (float): The time range in days.
		currency (str): The currency code (e.g., 'BTC').

	Returns:
		dict: The comparison data.
	"""
	currency = currency.upper()
	url = f'{YADIO_API_URL}/compare/{float(time_range)}/{currency}'
	return response(url)

def ads(currency: str, side: str, limit: int) -> dict:
	"""
	Fetches market ads for the specified currency and side (buy/sell).

	Args:
		currency (str): The currency code (e.g., 'BTC').
		side (str): The market side ('buy' or 'sell').
		limit (int): The maximum number of ads to fetch.

	Returns:
		dict: The market ads data.
	"""
	currency = currency.upper()
	url = f'{YADIO_API_URL}/market/ads?currency={currency}&side={side}&limit={int(limit)}'
	return response(url)

def stats(currency: str, side: str) -> dict:
	"""
	Fetches market statistics for the specified currency and side (buy/sell).

	Args:
		currency (str): The currency code (e.g., 'BTC').
		side (str): The market side ('buy' or 'sell').

	Returns:
		dict: The market statistics.
	"""
	currency = currency.upper()
	url = f'{YADIO_API_URL}/market/stats?currency={currency}&side={side}'
	return response(url)

def ping() -> str:
	"""
	Checks the status of the Yadio API.

	Returns:
		str: The API status ('ok' if operational).
	"""
	url = f'{YADIO_API_URL}/ping'
	return response(url)['status']

#################
##### Extra #####
#################

def midnight_price(currency: str, timezone: str = None) -> float:
	"""
	Fetches the price of the specified currency at midnight in the given timezone.

	Args:
		currency (str): The currency code (e.g., 'BTC').
		timezone (str, optional): The timezone to use (e.g., 'America/Sao_Paulo').

	Returns:
		float: The price at midnight, or None if not found.
	"""
	# Get the current time in the specified timezone or local time
	if timezone:
		tz = pytz.timezone(timezone)
		now = datetime.now(tz)
	else:
		now = datetime.now()

	# Fetch the exchange rates for the last hour
	data = today(now.hour + 1, currency)
	if not data:
		return None

	# Filter the entries to find the price at midnight
	midnight_entries = [entry for entry in data if datetime.strptime(entry["time"], "%I:%M %p").time().minute == 0]
	return midnight_entries[-1]["price"] if midnight_entries else None

def daily_price_var(currency: str, timezone: str = None) -> float:
	"""
	Calculates the daily price variation for the specified currency.

	Args:
		currency (str): The currency code (e.g., 'BTC').
		timezone (str, optional): The timezone to use (e.g., 'America/Sao_Paulo').

	Returns:
		float: The daily price variation as a percentage, or None if an error occurs.
	"""
	# Get the current exchange rate
	current_rate_data = convert(1, 'BTC', currency)
	if not current_rate_data or "rate" not in current_rate_data:
		raise ValueError("Error fetching the current exchange rate.")

	current_rate = current_rate_data["rate"]

	# Get the opening rate (midnight price)
	opening_rate = midnight_price(currency, timezone)
	if not opening_rate:
		raise ValueError("Error fetching the opening exchange rate.")

	# Calculate the price variation
	price_change = (current_rate / opening_rate) - 1
	return price_change

def min_price(hours: float, currency: str) -> dict:
	"""
	Finds the entry with the minimum price from the data returned by `today`.

	Args:
		hours (float): The number of hours to fetch data for.
		currency (str): The currency code (e.g., 'BRL').

	Returns:
		dict: The entry with the minimum price, or None if no data is available.
	"""
	data = today(hours, currency)
	if not data:
		return None

	# Find the entry with the minimum price
	min_entry = min(data, key=lambda x: x["price"])
	return min_entry

def max_price(hours: float, currency: str) -> dict:
	"""
	Finds the entry with the maximum price from the data returned by `today`.

	Args:
		hours (float): The number of hours to fetch data for.
		currency (str): The currency code (e.g., 'BRL').

	Returns:
		dict: The entry with the maximum price, or None if no data is available.
	"""
	data = today(hours, currency)
	if not data:
		return None

	# Find the entry with the maximum price
	max_entry = max(data, key=lambda x: x["price"])
	return max_entry

def parse_time(time_str: str, date: datetime) -> datetime:
	"""
	Converts a time string (e.g., '3:45 AM') to a datetime object using the provided date.

	Args:
		time_str (str): The time string in 12-hour format (e.g., '3:45 AM').
		date (datetime): The date to associate with the time.

	Returns:
		datetime: The combined datetime object.
	"""
	time_format = "%I:%M %p"
	time_obj = datetime.strptime(time_str, time_format).time()
	return datetime.combine(date, time_obj)

def volatility(hours: int, currency: str, timezone: str = None) -> float:
	"""
	Calculates the volatility of a currency over a specified time range (percentage difference between the max and min price).
	The result can be positive (increase) or negative (decrease), depending on which price is more recent.

	Args:
		hours (int): The number of hours to fetch data for (1 to 24).
		currency (str): The currency code (e.g., 'BRL').
		timezone (str, optional): The timezone to use (e.g., 'America/Sao_Paulo').

	Returns:
		float: The volatility as a percentage (decimal rounded to 5 places), or None if an error occurs.
	"""
	if hours < 1 or hours > 24:
		raise ValueError("Hours must be between 1 and 24.")

	# Get the current date and time in the specified timezone or local time
	if timezone:
		tz = pytz.timezone(timezone)
		now = datetime.now(tz)
	else:
		now = datetime.now()

	# Fetch the entries with the min and max prices
	min_entry = min_price(hours, currency)
	max_entry = max_price(hours, currency)

	if not min_entry or not max_entry:
		return None

	# Parse the times of the min and max prices
	min_time_str = min_entry["time"]
	max_time_str = max_entry["time"]

	# Determine the date for each time
	min_time = parse_time(min_time_str, now.date())
	max_time = parse_time(max_time_str, now.date())

	# Adjust for cases where the time crosses midnight
	if min_time > now:
		min_time -= timedelta(days=1)
	if max_time > now:
		max_time -= timedelta(days=1)

	# Extract the prices
	min_p = min_entry["price"]
	max_p = max_entry["price"]

	# Determine which price is more recent
	if max_time > min_time:
		volatility_value = (max_p - min_p) / min_p
	else:
		volatility_value = (min_p - max_p) / max_p

	# Round the result to 5 decimal places
	return round(volatility_value, 5)