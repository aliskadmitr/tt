import json
import csv

import requests
from bs4 import BeautifulSoup

# Сохраняем ссылку, содержащую в себе категории продуктов
url = "https://health-diet.ru/"

header = {
    "Accept": "*/*",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"
}

# Получаем код HTML-страницы
req = requests.get(url, headers=header)
src = req.text

# Сохраняем код HTML-страницы в файл
with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)

# Сохраним код страницы в переменную
with open("index.html", encoding="utf-8") as file:
    src = file.read()
    soup = BeautifulSoup(src, "lxml")

# Создадим переменную, которая будет хранить в себе все ссылки на категории продукты
all_products_href = soup.find_all(class_="mzr-tc-group-item-href")

# Создадим словарь, который будет хранить имя категории и соответствующую ей ссылку
all_products_dict = {}
for product in all_products_href:
    product_text = product.text
    product_href = "https://health-diet.ru" + product.get("href")
    all_products_dict[product_text] = product_href

#Сохраним словарь в JSON файл
with open("all_products_dict.json", "w", encoding="utf-8") as file:
    #Записываем содержимое в файл
    json.dump(all_products_dict, file, indent=4, ensure_ascii=False)

#Сохораняем содержимое файла в переменную
with open("all_products_dict.json", encoding="utf-8") as file:
    all_products = json.load(file)
# #Счетчик страниц
count = 0

#На каждой итерации цикла заходим в категорию и собираем информацию о товаре
for item_name, item_href in all_products.items():
    #Заменяем определенные символы на _
    res = ['.', ',', '-', '?', '/']
    for symbol in res:
        if symbol in item_name:
            item_name = item_name.replace(symbol, "_")

    #Переходим к запросам на странице
    req = requests.get(url = item_href, headers=header)
    src = req.text

    #Сохраняем страницу под именем категории в файл
    with open(f"data/{count}_{item_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    #Открываем и сохраняем страницу в переменную
    with open(f"data/{count}_{item_name}.html", encoding="utf-8") as file:
        src = file.read()
    print(src)
    soup = BeautifulSoup(src, "lxml")
    #comment

        #Создае папку data для хранения этих страниц

    #Собираем заголовки таблицы в список
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    #Извлекаем из списка конкретные заголовки
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    #Файл будет создан или перезаписан, если он уже существует. ежим "w" указывает на то, что файл будет открыт для записи
    with open(f"data/{count}_{item_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Указываем писателю, что записывать в файл
        writer.writerow(
            (product,
            calories,
            proteins,
            fats,
            carbohydrates)
            )

    #Собираем данные продуктов
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    for item in products_data:
        products_tds = item.find_all("td")
        title = products_tds[0].find("a").text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text
        print(proteins)

    count+=1


