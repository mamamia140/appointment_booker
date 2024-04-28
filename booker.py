from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email_sender import MailServer
from dotenv import load_dotenv
import time
import os

SITE_URL = "https://itfrandevu.istanbul.edu.tr/?a=1"

INPUT_FIELDS = {
    'TC': '//*[@id="idnumber"]',
    'PHONE': '//*[@id="phonenumber"]',
    'FATHER_NAME': '//*[@id="fathername"]',
    'BIRTH_DATE': '//*[@id="birthyear"]',
    'SECURITY_CODE_INPUT': '//*[@id="securitycode"]'
}

element_xpaths = [
    '/html/body/div[1]/div/div[1]/button',
    '//*[@id="login"]',
    '//*[@id="OgretimUyeRandevu"]',
    '/html/body/div/div[7]/div/div/div[3]/div/div/span',
    '/html/body/div/div[5]/div/div[2]/ul/li[3]'
]

load_dotenv()
opts = FirefoxOptions()
mailserver = MailServer()
mailserver.authenticate()

def get_env_var(name):
    return os.getenv(name)

def fill_in_the_blanks(driver):
    for key, xpath in INPUT_FIELDS.items():
        if key == 'SECURITY_CODE_INPUT':
            driver.find_element(By.XPATH, xpath).send_keys(driver.find_element(By.XPATH, '//*[@id="SecureImage"]').get_attribute("data-val"))
        else:
            driver.find_element(By.XPATH, xpath).send_keys(get_env_var(key))

def navigate_to_the_ent_appointments(driver):
    for xpath in element_xpaths:
        try:
            time.sleep(5)
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except Exception as e:
            raise e
    

def get_the_list_of_doctors(driver):
    return driver.find_element(By.XPATH, '/html/body/div/div[6]/div/ul').find_elements(By.TAG_NAME,"li")

def check_if_there_is_available_appointment_slot(list_of_doctors):
    print("checking")
    list_of_available_doctors = ""
    for li in list_of_doctors:
        doctor, state = li.find_elements(By.TAG_NAME,'span')
        if(state.text != "Dolu"):
            list_of_available_doctors = list_of_available_doctors + doctor.get_attribute("data-poliklinik") + "\n"
            print("Doctor:{}, State:{}".format(doctor.get_attribute("data-poliklinik"), state.text))
    
    if(list_of_available_doctors != ""):
        mailserver.message.set_content("List of available doctors:\n" + list_of_available_doctors)
        mailserver.send_mail()

def task():
    driver = webdriver.Firefox(options=opts)
    driver.get(SITE_URL)
    try:
        fill_in_the_blanks(driver)
        navigate_to_the_ent_appointments(driver)
        check_if_there_is_available_appointment_slot(get_the_list_of_doctors(driver))
    except Exception as e:
        print(f"An error was encountered while navigating to the appointment page\nERROR message: {e.msg}")
    finally:
        print("Closing the driver")
        driver.quit()
