from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

#Chromium Path
PATH = os.environ.get["CHROMIUM_PATH"]
#Linkedin Login Email
EMAIL = os.environ.get["EMAIL"]
#Linkedin Login Password
PASSWORD = os.environ.get["PASSWORD"]


driver = webdriver.Chrome(executable_path=PATH)

driver.get(url="https://www.linkedin.com/jobs/search/?f_E=2%2C3%2C1&f_LF=f_AL&geoId=102748797&keywords=Data Analyst&location=Texas%2C%20United%20States&sortBy=R")

sign_in = driver.find_element_by_link_text("Sign in")
sign_in.click()

username = driver.find_element_by_css_selector("#username")
username.send_keys(EMAIL)

password = driver.find_element_by_id("password")
password.send_keys(PASSWORD)


click_to_sign_in = driver.find_element_by_css_selector(".btn__primary--large")
click_to_sign_in.click()

time.sleep(4)

scr1 = driver.find_elements_by_class_name("jobs-search-results__list")
driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)


time.sleep(3)

easy_apply = driver.find_elements_by_class_name("job-card-container__apply-method")
print(easy_apply)
time.sleep(1)

stop = 25
while stop < 1000:
    print("called")
    for job in easy_apply:

        job.click()
        time.sleep(2)

        # Try to locate the apply button, if can't locate then skip the job.
        try:
            apply_button = driver.find_element_by_css_selector(".jobs-s-apply button")
            apply_button.click()
            time.sleep(3)


            submit_button = driver.find_element_by_css_selector("footer button")

            # If the submit_button is a "Next" button, then this is a multi-step application, so skip.
            if submit_button.get_attribute("data-control-name") == "continue_unify":
                close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                close_button.click()
                time.sleep(2)
                discard_button = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
                discard_button.click()
                print("Complex application, skipped.")
                continue
            else:
                submit_button.click()

            # Once application completed, close the pop-up window.
            time.sleep(2)
            close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
            close_button.click()
            try:
                time.sleep(driver.find_element_by_class_name("artdeco-modal__dismiss").click())
            except:
                pass

        # If already applied to job or job is no longer accepting applications, then skip.
        except NoSuchElementException:
            print("No application button, skipped.")
            continue

    stop += 25
    URL = f"https://www.linkedin.com/jobs/search/?f_E=2%2C3%2C1&f_LF=f_AL&geoId=102748797&keywords=python&location=Texas%2C%20United%20States&sortBy=R&start={stop}"
    driver.get(url=URL)

    time.sleep(4)

    scr1 = driver.find_elements_by_class_name("jobs-search-results__list")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)

    time.sleep(4)

    easy_apply = driver.find_elements_by_class_name("job-card-container__apply-method")
    print(stop)
print("Done")
