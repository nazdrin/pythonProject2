import asyncio
import logging
from aiogram.utils import executor
from data_base import sqlite_db
from create_bot import dp
from handlers import client, admin
import aioschedule

logging.basicConfig(level=logging.INFO)

async def morning_report():# Скрипт запускаемый по рассписанию
    await admin.report_1()

async def scheduler():# расписание запуска скрипта
    aioschedule.every().day.at("9:00").do(morning_report)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
async def on_startup(_): # запуск хендлеров, подтверждение запуска бота, запуск рассписания
    sqlite_db.sql_start()
    print('Привет')
    admin.register_handler_admin(dp)
    client.register_handler_client(dp)
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

