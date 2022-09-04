from enum import Enum
#import keyboards

# path and files
database_path = "database.db"
welcome_sticker_path = "img/sticker.webp"


# user statuses
class UserStatus(Enum):
    user_find = "Пользователь найден"
    user_not_find = "Пользователь не найден"
    user_successful_register = "Пользователь успешно зарегистрирован"


GOOGLE_PROJECT_ID = 'carmodelagent-cpgm'




