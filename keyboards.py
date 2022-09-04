from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import payment

def get_main_keyboard():    

    keyboard = InlineKeyboardMarkup()

    search_button = InlineKeyboardButton(text="Поиск", callback_data='search')
    about_button = InlineKeyboardButton(text="О нас", url='www.modellisimo.ru')
    random_button = InlineKeyboardButton(text="Показать случайную модель", callback_data='random')
    
    keyboard.add(search_button, random_button)
    keyboard.add(about_button)
    return keyboard

def get_back_to_main_menu_keyboard():    

    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text="Назад", callback_data='back_to_menu')
   
    keyboard.add(back_button)
    return keyboard

def payment_keyboard(item):
    keyboard = InlineKeyboardMarkup()

    pay_button = InlineKeyboardButton(text="Купить", url=payment.payment_for_item(item=item))

    keyboard.add(pay_button)
    return keyboard






