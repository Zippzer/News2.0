import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from keyboards import get_main_menu
from handlers.create_post import create_post
from handlers.delete_post import del_post
from db.db_connet import init_db
from service import token_env


API_TOKEN = token_env.token_bot


init_db()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message:types.Message):
    await message.answer('Выберите действие', reply_markup=get_main_menu())


async def main():
    dp.include_router(create_post)
    dp.include_router(del_post)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())