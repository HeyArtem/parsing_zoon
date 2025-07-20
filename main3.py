from selenium import webdriver
import time
from auth_data import password, url, user_name
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def start():
    try:
        driver = webdriver.Chrome()
        driver.get(url=url)
        time.sleep(2)

        # Ввод 'email'
        elem = driver.find_element(By.NAME, 'email')
        elem.clear()
        elem.send_keys(user_name)
        time.sleep(2)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)

        # Ввод 'password'
        elem = driver.find_element(By.NAME, 'pwd')
        elem.clear()
        elem.send_keys(password)
        time.sleep(2)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)

        # Убрать модальное окно
        elem.send_keys(Keys.ESCAPE)
        time.sleep(20)

        # elem = driver.find_element(By.CLASS_NAME, 'ModalStep-module__O5EZhW__closeButton')
        # elem.send_keys(Keys.RETURN)
        # time.sleep(3)





    except Exception as ex:
        print('ex: ', ex)
    finally:
        # закроет одну вкладку
        driver.close()
        # закроет браузер
        driver.quit()


def main():
    start()

if __name__ == '__main__':
    main()