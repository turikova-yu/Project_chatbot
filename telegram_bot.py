from dotenv import load_dotenv
import os
from telebot import TeleBot
import db
import keyboards
from locales.ru import BOT_TEXT
import config
import payment
import dialog_flow

db = db.Database(config.database_path)

path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path): # проверка существования пути
    load_dotenv(path)

token=os.getenv("TELEGRAM_TOKEN")   
if token:
    bot = TeleBot(token=os.getenv("TELEGRAM_TOKEN")) # создаем телебота
else:
    raise Exception("Неверный токен")

def get_welcome_sticker(): #метод для отправки приветственного стикера
    with open(config.welcome_sticker_path, 'rb') as file:
        return file.read()

def send_main_menu_message(message): # метод для отправки основной клавиатуры "Выберите пункт меню"
    keyboard = keyboards.get_main_keyboard()
    bot.send_message(
        chat_id=message.chat.id, 
        text=BOT_TEXT['main_menu'], 
        reply_markup=keyboard
    )


@bot.message_handler(commands=['start']) # то, что происходит после нажатия пользователем кнопки Старт
def welcome(message):
    user = message.from_user

    if db.user_exists(user_id=user.id):
        print('Пользователь найден')
    else:
        print('Пользователь не найден')
        db.add_user(name=user.first_name, telegram_id=user.id)
        print('Пользователь успешно зарегистрирован')
    sticker = get_welcome_sticker()
    bot.send_sticker(chat_id=message.chat.id, sticker=sticker)
    bot.send_message(
        chat_id=message.chat.id,
        text=BOT_TEXT['welcome_message'].format(user.first_name)
    )
    send_main_menu_message(message) # отправляется основная клавиатура Выберите пункт меню


def send_item_info(id, item): # метод для отправки информации о товаре
    message = BOT_TEXT['item_info'].format(item.name, item.description, item.price)
    bot.send_photo(chat_id=id, photo=item.photo, caption=message)

  


# обработчик текстового сообщения

@bot.message_handler(content_types='text') # вывод информации о товаре после введенного пользователем тега
def search_figure(message):
    item_name = dialog_flow.detect_intent_texts(config.GOOGLE_PROJECT_ID, 3, message.text, 'ru') 
    items_right = db.find_by_tag(message.text.lower())
    items_correct = db.find_by_tag(item_name)
        
    for item in items_right:
        send_item_info(message.chat.id, item) 
        keyboard = keyboards.payment_keyboard(item) # кнопка Купить
        bot.send_message(
            chat_id=message.chat.id, 
            text=BOT_TEXT['payment_info'],          # текст Для покупки нажмите кнопку
            reply_markup=keyboard)                  # вывод кнопки Купить

        payment.payment_for_item(item)              # метод для отправки формы оплаты

    for item in items_correct:
        send_item_info(message.chat.id, item) 
        keyboard = keyboards.payment_keyboard(item) # кнопка Купить
        bot.send_message(
            chat_id=message.chat.id, 
            text=BOT_TEXT['payment_info'],          # текст Для покупки нажмите кнопку
            reply_markup=keyboard)                  # вывод кнопки Купить

        payment.payment_for_item(item) 





# обработчик колбэков

@bot.callback_query_handler(func=lambda call:True)
def button_handler(call):
    keyboard = keyboards.get_back_to_main_menu_keyboard()
    message = call.message
    match call.data:
        case 'search':
            bot.edit_message_text(
                text=BOT_TEXT['enter_request'],
                chat_id=message.chat.id,
                message_id=message.id,
                reply_markup=keyboard
            )

        case 'random':
            item = db.find_random()
            send_item_info(message.chat.id, item)
            keyboard = keyboards.payment_keyboard(item) # кнопка Купить
            bot.send_message(
                chat_id=message.chat.id, 
                text=BOT_TEXT['payment_info'],          # текст Для покупки нажмите кнопку
                reply_markup=keyboard)                  # вывод кнопки Купить
            payment.payment_for_item(item)

        case 'back_to_menu':
            send_main_menu_message(message)
            bot.delete_message(message.chat.id, message.id)


bot.polling(non_stop=True) # чтобы бот постоянно работал