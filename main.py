import asyncio
from aiogram import Bot, Dispatcher, types
from handlers.user_handlers import register_user_handlers
from handlers.todo_handlers import register_todo_handlers
from decouple import config


class HandlerRegisterInterface:
    """ Register handlers """
    def register_handler(self, dispatcher: Dispatcher) -> None:
        register_user_handlers(dispatcher)
        register_todo_handlers(dispatcher)
        

class TelegramBotInterface:
    """ Bot entry point """
    async def main(self) -> None:
        bot = Bot(config("TOKEN_API"))
        dispatcher = Dispatcher(bot)
        HandlerRegisterInterface().register_handler(dispatcher)
        
        try:
            await dispatcher.start_polling()
        except Exception as _ex:
            return f"There is an exception - {_ex}"


if __name__ == "__main__":
    asyncio.run(TelegramBotInterface().main())