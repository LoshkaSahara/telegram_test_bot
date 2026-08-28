import requests
import random
import os

DEFAULT_ADDRESS = "https://nekos.best/api/v2"
HEADERS = {'user-agent': 'my-app/0.0.1'}
PARAMS = {
    "query":"",
    "type":0,
    "category":""
    }

# Открытие сессии
def session_open():
    session = requests.Session()
    return session

# Закрытие сессии
def session_close(session):
    session.close

# GET запрос
def get_querry(session, endpoint, params={}):
    response = session.get(f"{DEFAULT_ADDRESS}{endpoint}",
                           headers=HEADERS, params=params)
    print("—" * 120)
    print(f"Запрос на эндпоинт: {endpoint}")
    print(f"Статус ответа: {response.status_code}")
    print(f"Текст ответа ответа: {response.reason}")
    return response

# Получение случайной категроии
def rand_category(categories):
    categories_list = ''
    categories_list = random.choice(list(categories.keys()))
    return categories_list

# Создание стандартной папки для скачивания фалов
def create_defeault_download_folder():
    if not os.path.exists("Downloads"):
        os.mkdir("Downloads")
        
# Скачивание файла
def content_save(session, url):
    if url[-3:] == "png":
        file_name = os.path.join("Downloads", "image.png")
    elif url[-3:] == "gif":
        file_name = os.path.join("Downloads", "image.gif")
    
    try:
        response = session.get(url, stream=True, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # В сообщении будет статус и URL
        print("—" * 120)
        print("При скачивании изображения возникла ошибка:")
        print(f"Ошибка при запросе: {e}") 
        print(f"Код: {response.status_code}")
        print(f"Причина: {response.reason}")
        print(f"URL: {response.url}")
        return
        
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Файл сохранён -  {file_name}")
    return file_name

# Удаление файла
def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print("—" * 120)
        print(f"✅ Файл удален: {file_name}")
    else:
        print("—" * 120)
        print(f"❌ Файл не найден: {file_name}")

def get_content_type(url):
    if url[-3:] == "png":
        return "png"
    elif url[-3:] == "gif":
        return "gif"
        
def main():
    # Создание базовой папки для скачивания файлов
    create_defeault_download_folder()
    
    # Открытие сессии
    session = session_open()
    
    # Получение списка всех доступных эндпоинтов
    get_endpoints = get_querry(session, "/endpoints")
    # print(get_endpoints.text)
    
    # Получение случайной категории из полученного списка эндпоинтов
    random_category_name = rand_category(get_endpoints.json())
    # print(f"Случайная категория - {random_category_name}")

    # Получение случайного png или gif
    random_png_or_gif = get_querry(session, f"/{random_category_name}")
    # print(random_png_or_gif.text)

    # Получение данных из ответа случайной категории
    result = random_png_or_gif.json().get("results", "")
    anime_name = result[0].get("anime_name", "Unknown")
    artist_name = result[0].get("artist_name", "Unknown")
    if anime_name != "Unknown":
        print(f"Название аниме - {anime_name}")
    elif artist_name != "Unknown":
        print(f"Имя художника - {artist_name}")
    content_url = result[0].get("url", "Unknown")
    print(get_content_type(content_url))
    
    # Сохранение файла
    file_name = content_save(session, content_url)
    if file_name != None:
        remove_file(file_name)
    else:
        print("Файла для удаления не существует")
    
    session_close(session)


if __name__ == "__main__":
    main()
