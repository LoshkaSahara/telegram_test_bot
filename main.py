from config import API_TOKEN
from neko_best_requests import *
import telebot

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    ...

@bot.message_handler(commands=['help'])
def help_command(message):
    ...
    
@bot.message_handler(commands=['anime'])
def send_anime(message):
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
        caption = f"Название аниме - {anime_name}"
    elif artist_name != "Unknown":
        print(f"Имя художника - {artist_name}")
        caption = f"Имя художника - {artist_name}"
    content_url = result[0].get("url", "Unknown")
    # print(f"Формат скачанного файла - {get_content_type(content_url)}")
        
    # Сохранение файла
    file_name = content_save(session, content_url)
    content_type = get_content_type(content_url)
    
    #TODO добавить try на отправку сообщений. Телеграм блочит слишком частые запросы
    # Проверка: если файл png, то отправляется фотка, если gif - гифка
    if content_type == "png":
        if file_name and isinstance(file_name, str) and os.path.exists(file_name):
            with open(file_name, "rb") as photo_file:
                try:
                    bot.send_photo(message.chat.id, photo=photo_file, caption=caption)
                except Exception as e:
                    print(f"❌Не удалось отправить картинку.\nТекст ошибки - {e}")
                    bot.send_message(message.chat.id, f"❌Не удалось отправить картинку.\nТекст ошибки - {e}")
                    
            if file_name != None:
                remove_file(file_name)
            else:
                print("❌Файла для удаления не существует")
        else:
            bot.send_message(message.chat.id, "❌Не удалось найти или сохранить файл.")


    elif content_type == "gif":
        if file_name and isinstance(file_name, str) and os.path.exists(file_name):
            with open(file_name, "rb") as gif_file:
                try:
                    bot.send_animation(message.chat.id, animation=gif_file, caption=caption)
                except Exception as e:
                    print(f"❌Не удалось отправить гиф.\nТекст ошибки - {e}")
                    bot.send_message(message.chat.id,f"❌Не удалось отправить гиф.\nТекст ошибки - {e}")
            if file_name != None:
                remove_file(file_name)
            else:
                print("❌Файла для удаления не существует")
        else:
            bot.send_message(message.chat.id, "❌Не удалось найти или сохранить файл.")

            

    session_close(session)
    
bot.infinity_polling()