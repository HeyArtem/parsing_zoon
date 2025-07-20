mkdir selenium_start
cd selenium_start 
python3 -m venv venv 
source venv/bin/activate

brew update        # Обновляет информацию о доступных пакетах
brew upgrade       # Обновляет установленные пакеты
brew cleanup       # Удаляет старые версии пакетов аналогичен sudo apt autoremove && sudo apt autoclean.
	просто используй brew update && brew upgrade
pip install -U pip setuptools selenium
pip install -U requests bs4 lxml
pip install pandas
pip install openpyxl

touch main.py



по curl получение cookies, headers, response 
https://sqqihao.github.io/trillworks.html


возникла ошибка (в работающем проекте), сайт перестал отдавать данные

		# Поиск не вывода
        print('Status code:', response.status_code)		#Status code: 103
        print("response.text: ",response.text[:1000])		ничего
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)		ничего
            
❗ На каком-то этапе сайт перестал мне отдавать инфу на request-ах и я долго подбирая, нашел склад User Agent
[https://8500.ru/user-agent/]
и сайт мне начал отдавать. Если часто парсить с таким User-Agent ом — сайт может заподозрить, что это не настоящий бот Яндекса


Правила безопасности:
▫️ fake_useragent
	pip install fake_useragent
	
	from fake_useragent import UserAgent
	headers = {
	    "User-Agent": ua.random
	}
	
▫️ Случайные паузы
	time.sleep(random.uniform(2, 5))
	Возвращает вещественное число от 2 до 5 (например: 3.78)
	Пауза будет плавной : 2.3 секунды → 4.1 секунды → 2.9 секунды и т.д.
	time.sleep(random.randrange(2, 4))
	
▫️ Использование cookies и сессии

▫️ verify=certifi.where()
	certifi — это обновляемый набор доверенных CA-сертификатов , который используется браузерами и другими приложениями.
	
	import requests
	import certifi
	
	response = requests.get(
	    url="https://zoon.ru ",
	    headers=headers,
	    cookies=cookies,
	    verify=certifi.where()  # вместо verify=True или verify=False
	)
	
		⚠️ Не используй verify=False
		Это опасно , потому что:
		
		Отключает проверку безопасности
		Может привести к MITM-атакам
		Сайт может начать тебя блокировать

▫️ Использование прокси Чтобы не использовать один IP постоянно

▫️ искать API сайта
	
	
	
	
▫️ Последовательный переход по страницам
	Сначала главная → потом карточка → потом следующая
	
	Имитация просмотра страницы: Например, сначала заходишь на карточку клиники, потом на отзывы, потом на фото

Расшифровка заголовков: 
	именно заголовки чаще всего определяют, человек ты или бот.
	headers = {
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	    'accept-encoding': 'gzip, deflate, br',
	    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
	    'cache-control': 'max-age=0',
	    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'document',
	    'sec-fetch-mode': 'navigate',
	    'sec-fetch-site': 'none',
	    'sec-fetch-user': '?1',
	    'upgrade-insecure-requests': '1',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36'
	}
	
+-----------------------------+--------------------------------------------------------------------------------------------------+
|         Заголовок           |                                                                     Описание                     |
+-----------------------------+--------------------------------------------------------------------------------------------------+
| accept                      | Какие типы данных (HTML, XML, JSON и т.д.) готов принять браузер                                 |
| accept-encoding             | Какие способы сжатия поддерживает браузер (gzip, deflate, br)                                    |
| accept-language             | Какой язык предпочитает пользователь (ru-RU = русский (Россия), en-US = английский (США))        |
| cache-control               | Кэширование: max-age=0 — просим не использовать старый кэш                                       |
| sec-ch-ua                   | Информация о браузере (название и версия)                                                        |
| sec-ch-ua-mobile            | Используется ли мобильное устройство? ?0 = нет                                                   |
| sec-ch-ua-platform          | На какой ОС работает браузер ("Windows", "Mac", "Linux", "Android", "iOS")                       |
| sec-fetch-dest              | Куда направлен запрос (document, empty, audio, video и др.)                                      |
| sec-fetch-mode              | Режим запроса (navigate, cors, no-cors, same-origin и др.)                                       |
| sec-fetch-site              | Откуда пришёл запрос (same-site, cross-site, none)                                               |
| sec-fetch-user              | Пользователь ли вызвал этот запрос (?1 = да, ?0 = нет)                                           |
| upgrade-insecure-requests   | Готов ли браузер обрабатывать безопасные запросы                                                 |
| user-agent                  | Идентификатор браузера, чтобы сервер понимал, кто к нему обращается                              |
+-----------------------------+--------------------------------------------------------------------------------------------------+


pip freeze > requirements.txt
touch .gitignore
README.md 



uniform
