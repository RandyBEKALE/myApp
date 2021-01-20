#from selenium import webdriver as web
from seleniumwire import webdriver as web
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E


from datetime import datetime as time
from datetime import date
import  time as tm

def loop(driver):
    i=0
    driver.implicitly_wait(16)
    wait=W(driver, 40)

    driver.find_element(By.XPATH,"//a[@onclick='javascript:accepter()']").click() # clique sur accepter du cookie
    wait.until(E.invisibility_of_element((By.XPATH, "//div[@id='cookies-banner']"))) # desactive le cookie
    erreur = ["The server returned an invalid or incomplete response.","No server is available to handle this request.",
              "502 Bad Gateway"]

    while True:
        H = time.now().strftime("%H:%M:%S")
        today = date.today()
        message = "Date : {}  | Heure : {}   \t-> pas de plage horaire \n".format(today, H)
        message2 = "Date : {}  | Heure : {}  \t-> il y a eu plage horaire \n".format(today, H)
        f = open("/home/dehn/Bureau/drivers/prefecture_{}.txt".format(today), 'a')

        try:
            if driver.find_element(By.XPATH, "//h1//*").text in erreur:
                tm.sleep(2)
                driver.refresh()
                print("refreshed")
                driver.get("https://www.meurthe-et-moselle.gouv.fr/booking/create/22259/0")



            elem = driver.find_element(By.XPATH, "//input[@id='condition']") # cocher sur la checkbox
            elem2 = driver.find_element(By.XPATH, "//input[@name='nextButton']")
            elem.click()
            tm.sleep(2)
            elem2.click()
            tm.sleep(10)

            wait.until(E.visibility_of_element_located((By.XPATH, "//input[@id='planning22263']")))
            elem3 = driver.find_element(By.XPATH, "//input[@id='planning22263']")
            elem4 = driver.find_element(By.XPATH, "//input[@name='nextButton']")
            elem3.click()
            tm.sleep(3)
            elem4.click()
            tm.sleep(10)
            wait.until(E.visibility_of_element_located((By.XPATH, "//div[@id='submit_Booking']")))
            toto = driver.find_element(By.XPATH, "//form[@id='FormBookingCreate']").text
            if  toto == "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement.":
                driver.find_element(By.XPATH, "//input[@value='Terminer']").click()
                f.write(message)
                tm.sleep(10)

            else:
                f.write(message2)
                break

        except NoSuchElementException:
            tm.sleep(25)
            driver.refresh()
            driver.get("https://www.meurthe-et-moselle.gouv.fr/booking/create/22259/0")
            print("prob object pas trouvé {}".format(i))
            i += 1
            continue
        else:
            tm.sleep(25)
            #print(driver.wait_for_request("https://www.meurthe-et-moselle.gouv.fr/booking/create/22259/*"))
            driver.refresh()
            driver.get("https://www.meurthe-et-moselle.gouv.fr/booking/create/22259/0")
            print("prob temps {}".format(i))

            i += 1
            tm.sleep(10)
            continue
        tm.sleep(300)
        f.close()


if __name__ == "__main__":

    driver = web.Firefox(
        executable_path='/home/dehn/Bureau/drivers/geckodriver')

    driver.get("https://www.meurthe-et-moselle.gouv.fr/booking/create/22259/0")
    #try:
    loop(driver)
    #except NoSuchElementException or TimeoutException:
    #    tm.sleep(2)
    #    driver.refresh()
    #    driver.get("https://www.meurthe-et-moselle.gouv.fr/booking/create/22259/0")
    #    print("y a eu une erreur à {}".format(time.now()))
    #    loop(driver)




