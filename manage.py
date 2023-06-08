#!/usr/bin/env python
import os
os.system("chmod +x manage.py")

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.user_handlers import register_user_handlers
from handlers.todo_handlers import register_todo_handlers
from decouple import config


class HandlerRegisterInterface:
    """ Register any handlers """
    def register_handler(self, dispatcher: Dispatcher) -> None:
        register_user_handlers(dispatcher)
        register_todo_handlers(dispatcher)
        

class TelegramBotInterface:
    """ Bot entry point """
    async def main(self) -> None:
        bot = Bot(config("TOKEN_API"))
        storage = MemoryStorage()
        dispatcher = Dispatcher(bot, storage=storage)
        HandlerRegisterInterface().register_handler(dispatcher)
        
        try:
            await dispatcher.start_polling()
        except Exception as _ex:
            return f"There is an exception - {_ex}"
        finally:
            await bot.close()
            await storage.close()
            await storage.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(TelegramBotInterface().main())
    except KeyboardInterrupt:
        asyncio.run(TelegramBotInterface().bot.close())
        asyncio.run(TelegramBotInterface().storage.close())
        asyncio.run(TelegramBotInterface().storage.wait_closed())