from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your ChromeDriver executable
chrome_driver_path = r'C:\path\to\chromedriver.exe'  # Replace with the actual path

# Set up the ChromeDriver service
service = Service(chrome_driver_path)

# Set up the WebDriver
driver = webdriver.Chrome(service=service)

# Define the URL for the stock (e.g., Apple Inc.)
url = "https://finance.yahoo.com/quote/AAPL/"

# Open the URL
driver.get(url)

# Wait for the page to load (adjust the sleep time if needed)
time.sleep(5)

# Scrape Analyst Recommendations
try:
    recommendations = driver.find_element(By.CLASS_NAME, "card-link yf-6z16fb")  # Update the class name
    print("Analyst Recommendations:", recommendations.text)
except Exception as e:
    print("Analyst Recommendations not found. Error:", e)

# Close the WebDriver
driver.quit()