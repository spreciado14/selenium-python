import csv
import logging
import time
from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Set up the web driver (replace the path with the actual path to your Chrome driver)
service = Service(executable_path="/usr/local/bin/chromedriver")  # Specify the full path
driver = webdriver.Chrome(service=service)

# Define the product to search for
product_amazon = "wireless mouse"
product_ebay = "wireless mouse"

# Function to extract product data from a website
def extract_amazon_product_data(url, search_term):
    driver.get(url)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.send_keys(search_term)
    search_box.submit()
    try:
        data = []
        # Wait for the search results page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item")))
    except TimeoutException:
        logging.error("No products found on Amazon with search term: " + search_term)
        # Find the product name and price elements for the top 5 products
    product_names = driver.find_elements(By.CSS_SELECTOR, ".a-size-medium.a-color-base.a-text-normal")[:3]
    product_prices = driver.find_elements(By.CSS_SELECTOR, ".a-offscreen")[:3]
    # Extract the text from these elements and print the product names and prices
    for name, price in zip(product_names, product_prices):
        data.append({"name": name.text, "price": price.text, "source": url})

    return data


def extract_ebay_product_data(url, search_term):
    driver.get(url)

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#gh-ac"))
    )
    search_box.send_keys(search_term)
    search_box.submit()

      # Locate the products
    try:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".srp-results .s-item"))
        )
    except TimeoutException:
        logging.error("No products found on eBay with search term: " + search_term)
        return []

    # Extract the product data
    data = []
    for product in products[:3]:
        try:
            name_element = product.find_element(By.CSS_SELECTOR, ".s-item__title")
            price_element = product.find_element(By.CSS_SELECTOR, ".s-item__price")
            name = name_element.text
            price = price_element.text
            data.append({"name": name, "price": price, "source": url})
        except NoSuchElementException:
            logging.error("Error extracting product data on eBay")
            return []  # Return an empty list when no products are found
        
    return data

# Extract product data from Amazon and eBay
amazon_data = extract_amazon_product_data("https://www.amazon.com", product_amazon)
ebay_data = extract_ebay_product_data("https://www.ebay.com", product_ebay)

# Combine the data from both websites
all_data = amazon_data + ebay_data

# Write the data to a CSV file
with open("product_comparison.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["name", "price", "source"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for product in all_data:
        writer.writerow(product)

# Close the web driver
driver.quit()