import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the web driver
service = Service(executable_path="/usr/local/bin/chromedriver")  # Specify the full path
driver = webdriver.Chrome(service=service)

# Open the Amazon home page
driver.get("https://www.amazon.com")

# Find the search bar element
search_bar = driver.find_element(By.ID, "twotabsearchtextbox")

# Input the search term into the search bar
search_term = "wireless headphones"
search_bar.send_keys(search_term)

# Submit the search
search_bar.submit()

# Wait for the search results page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item")))

# Find the product name and price elements for the top 5 products
product_names = driver.find_elements(By.CSS_SELECTOR, ".a-size-medium.a-color-base.a-text-normal")[:5]
product_prices = driver.find_elements(By.CSS_SELECTOR, ".a-offscreen")[:5]

# Extract the text from these elements and print the product names and prices
for name, price in zip(product_names, product_prices):
    print(f"Product Name: {name.text} | Price: {price.text}")

# Close the browser
driver.quit()