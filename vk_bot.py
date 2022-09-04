from dotenv import load_dotenv
import os
import db
from locales.ru import BOT_TEXT
import config
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

db = db.Database(config.database_path)

path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path): # проверка существования пути
    load_dotenv(path)

        
def check_user(message):
    user_id = message.get('from_id')

    if db.user_exists(user_id=user_id):
        print(config.UserStatus.user_find)
    else:
        print(config.UserStatus.user_not_find)

        name = vk.users.get(user_id=message.get('from_id'))[0]


        db.add_user(name=name['first_name'], vk_id=user_id)
        print(config.UserStatus.user_successful_register) 

        
    #bot.send_sticker(chat_id=message.chat.id, sticker=sticker)
        vk.messages.send(
            user_id=user_id, 
            message=BOT_TEXT['welcome_message'].format(name['first_name']), 
            random_id=0
        )
    #send_main_menu_message(message)    


vk_session = VkApi(token=os.getenv("VK_TOKEN"))
vk = vk_session.get_api()
group_id = os.getenv("GROUP_ID")
longpoll = VkBotLongPoll(vk=vk_session, group_id=group_id)

for event in longpoll.listen(): # прослушка нашей группы
    if event.type == VkBotEventType.MESSAGE_NEW:
        check_user(event.message)
       
       

   