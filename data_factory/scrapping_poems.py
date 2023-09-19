#!pip install selenium

import random
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

##########
########## WARNINGS
##########

print("Need to check that your driver version is compatible with your navigator.")


##########
########## SCRAPPING FUNCTIONS
##########

# Specify where Driver is located on computer
DRIVER_PATH = r"C:\Users\sim13\OneDrive\Documents\chromedriver.exe"
BASE_URL = "https://www.bonjourpoesie.fr/lesgrandsclassiques"
MAIN_XPATH = "/html/body/main/div/div[1]/div[2]/form/div[3]/div/button"
ALL_POEMS_XPATH = "/html/body/main/div/div[2]/div/div/div/ul/li"
BEGIN = 154  # How many poems have already been scrapped in order to achieve scrappinf in multiple times


def launch_driver(
    BASE_URL=BASE_URL, MAIN_XPATH=MAIN_XPATH, ALL_POEMS_XPATH=ALL_POEMS_XPATH
):
    """
    Launch driver and achieve scrapping

    Parameters
    ----------
    BASE_URL: website url by default
        need to keep the Url as written here in order for this specific function to work.

    MAIN_XPATH: xpath, MAIN_XPATH by default
        xpath to find the button to get all poems in one page.

    ALL_POEMS_XPATH: xpath, ALL_POEMS_XPATH by default
        xpath to find the actual number of poems of main page.

    Returns
    -------
    string
        flag signalling that drivers has quitted.
    """

    options = Options()
    options.headless = True
    options.add_argument("--headless")  # no display of the chrome window
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    ###
    ### A loop to get all poems from the BASE_URL above
    ### It will work only for this particular website cf html specifities
    ###

    driver.get(BASE_URL)
    driver.find_element_by_xpath(MAIN_XPATH).click()
    nb_poems = driver.find_elements_by_xpath(ALL_POEMS_XPATH)

    scrapping_poems(nb_poems=nb_poems)

    driver.quit()

    return "Driver Quits"


def scrapping_poems(nb_poems, driver, BASE_URL=BASE_URL, BEGIN=BEGIN):
    """
    Go to the website "bonjourpoesie.fr" and achieve scrapping of all poems

    Parameters
    ----------
    BASE_URL: website url by default
        need to keep the Url as written here in order for this specific function to work.

    BEGIN: integer, BEGIN by default
        how many poems have already been scrapped from this website.
        this parameter helps to achieve scrapping of all poems in multiple times.

    nb_poems: integer
        how many poems this function can get from the BASE_URL.

    driver: webdriver set with several options
        need to adapt DRIVER_PATH where the driver is located in local.

    Returns
    -------
    string
        flag signalling that scrapping is over. If not displayed, there has been a problem in scrapping and one can launch again using parameter BEGIN
    """
    assert nb_poems > BEGIN

    data = list()
    for i in range(BEGIN, len(nb_poems) + 1):
        try:
            driver.find_element_by_xpath(
                f"/html/body/main/div/div[2]/div/div/div/ul/li[{i+1}]/a"
            ).click()
        except:
            pass
        try:
            sleep(2 + random.randrange(3))
            poem_text = driver.find_element_by_xpath(
                "/html/body/main/div/section/div[1]"
            )
            poem_dates = driver.find_element_by_xpath(
                "/html/body/main/div/section/h3[1]"
            )
            data.append([poem_text.text, poem_dates.text])
            data_df = pd.DataFrame(data)
            data_df.to_csv(f"data_{BEGIN}.csv")
        except:
            pass
        # Go back on Welcome page
        driver.get(BASE_URL)
        driver.find_element_by_xpath(
            "/html/body/main/div/div[1]/div[2]/form/div[3]/div/button"
        ).click()

        sleep(1 + random.randrange(5))

    return "Scrapping Over"


##########
########## LAUNCH SCRAPPING WITH PREVIOUS FUNCTIONS
##########

launch_driver()
