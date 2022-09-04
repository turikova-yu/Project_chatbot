from pyqiwip2p import QiwiP2P
import os
from dotenv import load_dotenv



path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path): # проверка существования пути
    load_dotenv(path)


p2p = QiwiP2P(auth_key=os.getenv("QIWI_PRIVATE_KEY"))

def payment_for_item(item):
    
    new_bill = p2p.bill(amount=item.price, lifetime=120)

    print(new_bill.bill_id, new_bill.pay_url)

    bill = new_bill.pay_url

    return bill
