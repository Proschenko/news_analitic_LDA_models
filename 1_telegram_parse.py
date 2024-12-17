import os
import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
channel_username = os.getenv("CHANNEL")

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)

async def fetch_posts():
    await client.start(phone=phone)
    channel = await client.get_entity(channel_username)

    offset_id = 0
    limit = 1000  # Увеличиваем лимит сообщений за один запрос
    year_to_filter = 2024

    # Открываем файл для записи
    with open('telegram_posts_2024.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "date"])  # Заголовки столбцов

        total_messages = 0
        while True:
            # Запрашиваем сообщения
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))

            if not history.messages:
                break

            # Записываем сообщения в CSV
            for message in history.messages:
                if message.date.year == year_to_filter and message.message:
                    writer.writerow([message.message.replace('\n', ' '), message.date.isoformat()])
                    total_messages += 1

            # Лог каждые 1000 сообщений
            if total_messages % 1000 == 0:
                print(f"{total_messages} сообщений собрано...")

            offset_id = history.messages[-1].id

    print(f"Всего сохранено {total_messages} сообщений!")

# Запуск
with client:
    client.loop.run_until_complete(fetch_posts())
