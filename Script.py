import json
# from datetime import datetime
import re

with open('operations.json', 'r', encoding='utf-8') as file:
    operations = json.load(file)


def format_card_number(card_number):
    text = re.search(r'\D+', card_number)
    payment_system = text[0]
    number = re.search(r'\d+', card_number)
    account_number = number[0]
    return f'{payment_system}{account_number[:4]} {account_number[5:7]}** **** {account_number[-4:]}'


def format_account_number(account_number):
    return f'**{account_number[-4:]}'


def format_date(date_operation):
    date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    formatted_date = re.sub(date_pattern, r'\3.\2.\1', date_operation[:10])
    # formatted_date = datetime.strptime(date_operation[:10], "%Y-%m-%d").strftime("%d.%m.%Y") с помощью модуля datetime
    return formatted_date


executed_operations = sorted(
    [op for op in operations if op.get('state')],
    key=lambda x: x['date'],
    reverse=True
)[:5]

for op in executed_operations:
    print(f"{format_date(op['date'])} {op.get('description', 'Описание отсутствует')}")
    print(f"{format_card_number(op.get('from', 'Отсутствует')) if 'from' in op else format_account_number(op['to'])}"
          f" -> Счет {format_account_number(op['to'])}")
    print(f"{op['operationAmount']['amount']} {op['operationAmount']['currency']['name']}\n")

