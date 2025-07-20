import os
import re
import csv
import time
import random
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote
import certifi
from auth_data import url_m2, headers, cookies


# todo Что такое цепочка действий ActionChains?


def get_sources_html(url):
    """
    Сохраняю html
    """
    driver = webdriver.Chrome()
    driver.maximize_window()  # Окно на max

    try:
        driver.get(url=url_m2)
        time.sleep(3)

        while True:
            # Буду скролить страницу, пока в 'catalog-button-showMore' не появится 'hasmore-text'
            find_more_element = driver.find_element(By.CLASS_NAME, 'catalog-button-showMore')

            if driver.find_elements(By.CLASS_NAME, 'hasmore-text'):

                if not os.path.exists("data"):
                    os.mkdir("data")

                file_path = "data/source_page.html"

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(driver.page_source)
                return file_path


            else:
                # Скроллинг
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(3)

    except Exception as ex:
        print('[!] ex: ', ex)
        return None

    finally:
        # закроет одну вкладку
        driver.close()
        # закроет браузер
        driver.quit()


def get_items_urls(file_path):
    """
    Сохраняю все urls из html
    """
    if not os.path.exists(file_path):
        print("[!] Файд не найден: ", file_path)
        return None

    with open(file_path, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    items_divs = soup.find_all('div', class_='minicard-item__info')

    urls = []
    for item in items_divs:
        try:
            item_url = item.find('div', class_='minicard-item__title').find('a').get('href')
            urls.append(item_url)
        except Exception as ex:
            print('[!] Не удалось получить url из карточки', ex)

    file_path_urls = "data/items_url.txt"

    # Записываю в файл все url, каждый с новой строки
    with open(file_path_urls, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(f"{url}\n")
    # print("[info] Urls collected successfully!")
    return file_path_urls


def get_data(file_path):
    """
    собираю данные из полученых url
    """
    if not os.path.exists(file_path):
        print('[!] Файл с URL-ми не найден!', file_path)
        return None

    with open(file_path) as file:
        # urls_list = file.readlines()
        #
        # clear_urls_list = []
        # for url in urls_list:
        #     url = url.strip()
        #     clear_urls_list.append(url)
        # print(clear_urls_list)

        # Замена на list comprehension
        urls_list = [url.strip() for url in file.readlines()]

    # для записи в csv
    all_data_csv = []

    # для записи в json & xlsx
    all_data_json_xlsx = []

    # счетчик карточек для вывода прогресса
    count = 1

    urls_count = len(urls_list)

    for url in urls_list[:3]:
        print('url:', url)
        response = requests.get(url=url, headers=headers, cookies=cookies, verify=certifi.where())
        # response = requests.get(url=url, headers=headers, cookies=cookies)



        # Поиск не вывода
        print('Status code:', response.status_code)
        print("response.text: ",response.text[:1000])
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, 'lxml')

        try:
            item_name = soup.find("span", {"itemprop": "name"}).text.strip()
            print('item_name:', item_name)
        except Exception as ex:
            item_name = None

        # Сбор телефонов (у кого-то из несколько)
        item_phones_list = []
        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="tel-phone")
            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as ex:
            item_phones = None

        try:
            item_address = soup.find("address", class_="iblock").text.strip()
        except Exception as ex:
            item_address = None

        # сайт и сети (у кого-то нет ни того, ни другого, у кого-то "сайт"/"оф сайт")
        # Регулярки!
        try:
            # item_site = soup.find('div', class_="service-maininfo").find(text=re.compile("Сайт|Официальный сайт")).find_next().text.strip()
            item_site = soup.find('span',
                                  class_="service-website-icon").find_next().find_next().find_next().text.strip()

            # item_site = soup.find('div', class_="service-maininfo").find(text=re.compile("Сайт|Официальный сайт")).find_next().find("a").get('href')
        except Exception as ex:
            item_site = None

        """
        Иногда есть class="js-service-socials "
        а в нем class="svg-socials-vk" & class="svg-socials-telegram"
        """
        social_networks_list = []
        try:
            # item_social_networks = soup.find('div', class_="service-description-social-list").find_next().find_all('a')
            item_social_networks = soup.find('div', class_="js-service-socials").find_all('a')
            for sn in item_social_networks:
                sn_url = sn.get('href')
                sn_url = unquote(sn_url)
                sn_url_clear = sn_url.split('?to=')[1].split('&hash')[0]
                social_networks_list.append(sn_url_clear)
        except Exception as ex:
            social_networks_list = None

        # для записи в json & excel строки со списками преобразовал в строки
        prepared_item_phones = ', '.join(item_phones_list) if isinstance(item_phones_list, list) else item_phones_list
        prepared_social_networks = ', '.join(social_networks_list) if isinstance(social_networks_list, list) else social_networks_list

        # для записи в csv строки со списками преобразовал в строки
        all_data_csv.append(
            [
                item_name,
                ', '.join(item_phones_list) if isinstance(item_phones_list, list) else item_phones_list,
                item_address,
                item_site,
                ', '.join(social_networks_list) if isinstance(social_networks_list, list) else social_networks_list
            ]
        )

        # print(
        #     f"Наименование: {item_name},\n Телефон: {item_phones_list},\n Адрес: {item_address},\n Сайт: {item_site},\n Соц.сети:{social_networks_list},\n {'-' * 10}")
        all_data_json_xlsx.append(
            {
                "Наименование": item_name,
                "Телефон:": prepared_item_phones,
                "Адрес:": item_address,
                "Сайт:": item_site,
                "Соц.сети": prepared_social_networks,
            }
        )



        time.sleep(random.uniform(2, 4))

        # После 10 итерации, увеличенная пауза
        if count % 10 == 0:
            time.sleep(random.uniform(2, 5))
        print(f"+Processed: {count} / {urls_count}")

        count += 1

    file_path_json = 'data/result.json'
    with open(file_path_json, 'w', encoding='utf-8') as file:
        json.dump(all_data_json_xlsx, file, indent=4, ensure_ascii=False)

    # Записываю в csv
    file_path_csv = 'data/result_csv.csv'
    # encoding='utf-8-sig'-кодировка для excel
    with open(file_path_csv, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Наименование',
                'Телефон',
                'Адрес',
                'Сайт',
                'Соц.сети',
            )
        )
        writer.writerows(all_data_csv)

    # Записываю в excel
    file_path_excel = 'data/result_excel.xlsx'
    df = pd.DataFrame(all_data_json_xlsx)
    df.to_excel(file_path_excel, index=False, engine='openpyxl')

    return file_path_json


def main():
    source_file = get_sources_html(url=url_m2)
    if not source_file:
        print('[!] Ошибка в get_sources_html. HTML не загружен!')
        return

    print("[info] HTML сохранен!")

    urls_file = get_items_urls(source_file)
    if not urls_file:
        print('[!] Ошибка в get_items_urls. URL-ы не собраны!')
        return

    print("[info] Urls collected successfully!")

    json_file = get_data(urls_file)
    if not json_file:
        print('[!] Ошибка в get_data. Данные не собраны!')
        return

    print("[info] Data collected successfully!")


if __name__ == '__main__':
    main()
