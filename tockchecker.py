import tkinter as tk
from tkinter import messagebox
from config import bot_token, bot_chatID
from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from datetime import date, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests
import time
import threading
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Tock Checker")
    parser.add_argument("-s", "--start-date", type=str, help="Start date in format YYYY-MM-DD", default=None)
    parser.add_argument("-e", "--end-date", type=str, help="End date in format YYYY-MM-DD", default="2023-11-01")
    parser.add_argument("-i", "--interval", type=int, help="Check interval in seconds", default=3600)
    return parser.parse_args()

# Function to find all Fridays and Saturdays between two dates
def find_fridays_and_saturdays(start_date, end_date):
    """
    Find all Fridays and Saturdays between two dates.
    """
    days = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in [4, 5]:  # 4 is Friday, 5 is Saturday
            days.append(current_date)
        current_date += timedelta(days=1)
    return days

def check_availability(start_date, end_date, check_interval):

    days_to_check = find_fridays_and_saturdays(start_date, end_date)
    days_to_check = find_fridays_and_saturdays(start_date, end_date)

    profile = profiles.Windows()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

def check_availability(start_date, end_date, check_interval):

    days_to_check = find_fridays_and_saturdays(start_date, end_date)

    profile = profiles.Windows()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    try:
        with Chrome(profile, options=options, uc_driver=False) as driver:

            wait = WebDriverWait(driver, 10)  # wait up to 10 seconds

            while True:
                try:
                    for day in days_to_check:

                        formatted_day = day.strftime("%Y-%m-%d")
                        print(f"Checking availability for {formatted_day}...")
                        driver.get(f'https://www.exploretock.com/deathcodc/experience/376796/death-co-reservation?cameFrom=search_modal&date={formatted_day}&showExclusives=true&size=2&time=19%30')
                        time_buttons = driver.find_elements(By.CLASS_NAME, "Consumer-resultsListItem")
                        available_times = []

                        # Wait for the first time button to load
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Consumer-resultsListItem")))

                        # Add a small delay (adjust the time as needed)
                        time.sleep(1)

                        time_buttons = driver.find_elements(By.CLASS_NAME, "Consumer-resultsListItem")
                        available_times = []

                        for button in time_buttons:
                            if "is-available" in button.get_attribute("class"):
                                time_text = button.find_element(By.CLASS_NAME, "MuiTypography-root").text
                                available_times.append(time_text)

                        if available_times:
                            send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text=Time found at Death and Co at {formatted_day} {available_times}: https://www.exploretock.com/deathcodc/experience/376796/death-co-reservation?cameFrom=search_modal&date={formatted_day}&showExclusives=true&size=2&time=19%30'
                            response = requests.get(send_text)
                            print(f"Finished checking for {formatted_day}. Found available times: {available_times}")
                        else:
                            print(f"Finished checking for {formatted_day}. No times found.")
                    print(f"Available times on {formatted_day}: {available_times}")

                except Exception as e:
                    print(f"Error occurred: {e}")
                    print(f"Error occurred: {e}. Waiting for 1 minute before restarting.")
                    time.sleep(60)  # Wait for 1 minute before restarting

                time.sleep(check_interval)  # Wait for the specified interval before checking again

    except WebDriverException as wde:
        print("An error occurred with the headless browser.")
        print(f"Error details: {wde}")
        sys.exit(1)
    finally:
        if driver:
            driver.quit()
if __name__ == "__main__":
    try:
        args = parse_arguments()
        start_date = date.fromisoformat(args.start_date) if args.start_date else date.today()
        end_date = date.fromisoformat(args.end_date)
        check_interval = args.interval

        checker_thread = threading.Thread(target=check_availability, args=(start_date, end_date, check_interval))
        checker_thread.start()
        checker_thread.join()
    except KeyboardInterrupt:
        print("Stopping script...")
        sys.exit(0)