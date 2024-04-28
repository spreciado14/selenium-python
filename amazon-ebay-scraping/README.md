# Amazon and eBay Product Scraper

This script uses Selenium to scrape product data from Amazon and eBay.

## Setup

1. Install Python: Download and install Python from [the official website](https://www.python.org/downloads/).

2. Install Selenium: Run `pip install selenium` in your terminal to install Selenium.

3. Set up WebDriver: Download the WebDriver for your browser (e.g., ChromeDriver for Chrome) and add its location to your system's PATH.

## Running the Script

1. Open your terminal and navigate to the directory containing the script.

2. Run `python main.py`.

The script will scrape product data from Amazon and eBay and combine the results. The product data includes the name, price, and source URL.

## Logging

The script logs events and errors to a file named `app.log`. If a product search yields no results or an error occurs during execution, the script will log the event.

## Error Handling

The script includes error handling for cases where a product search yields no results. If no products are found on Amazon or eBay with the given search term, the script will log an error message and continue execution.
