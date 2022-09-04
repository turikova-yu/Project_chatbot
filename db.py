# логика при работе с базой данных
import sqlite3
import random

# запрос к таблице пользователей
class Database:
    def __init__(self, db_path : str) -> None:
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id : int) -> bool:
        with self.connection:
            result = self.cursor.execute(
                f"""SELECT NAME
                    FROM USERS
                    WHERE TelegramID == {user_id}
                    or VKID == {user_id}"""
            ).fetchall()
        return len(result)

    def add_user(self, name, address="", telegram_id=0, vk_id=0):
        with self.connection:
            self.cursor.execute(
                f"""INSERT INTO USERS
                (NAME, ADDRESS, MONEY, TELEGRAMID, VKID)
                VALUES("{name}", "{address}", 0, 
                {telegram_id if telegram_id > 0 else 0},
                {vk_id if vk_id > 0 else 0})"""
            )

    def get_user_address(self, user_id): # получение адреса пользователя
        with self.connection:
            result = self.cursor.execute(
                f"""SELECT ADDRESS
                FROM USERS
                WHERE USERS.ID == {user_id}"""
            ).fetchone
        return result[0]

        # аналогично с получением баланса пользователя. Сделать!!!

    def get_cart_items_info(self, cart_id): # выводит информацию о товарах в корзине
        with self.connection:
            result = self.cursor.execute(
                f"""SELECT *
                FROM V_CARTS
                WHERE CARTID == {cart_id}"""
            ).fetchall()
        return result   

    def get_order(self, order_id): 
        with self.connection:
            result = self.cursor.execute(
                f"""SELECT *
                FROM v_Orders
                WHERE ID == {order_id}"""
            ).fetchall()
        return result   

    # реализуем поиск по тегам
    def get_items(self):
        with self.connection:
            items = self.cursor.execute(
                f"""SELECT *
                FROM Items"""
            ).fetchall()

        result = []
        for base_item in items:
            item = Item(
                base_item[0], 
                base_item[1],
                base_item[2],
                base_item[3],
                base_item[4],
                base_item[5] 
            )
            result.append(item)
        return result

# поиск по тэгу
    def find_by_tag(self, tag):
        items = self.get_items()
        result = []
        for item in items:
            if tag in item.tags:
                result.append(item)
        return result

# поиск случайного товара
    def find_random(self):
        items = self.get_items()
        a = random.choice(items)
        print(a)
        return a





class Item:
    def __init__(
        self, 
        id : int, 
        name : str, 
        description : str, 
        tags : str, 
        price : int, 
        photo : str
    ):
        self.id = id
        self.name = name
        self.description = description
        self.tags = tags.split(', ')
        self.price = price
        with open(f'img/{photo}', 'rb') as file:
            self.photo = file.read()
            #self.id = self.id[0]
            #self.name = self.name[0]

        



