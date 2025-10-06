from aiogram import Router, F
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import date
from db.CRUD import CreatePost
from db.db_connet import Session
from service import token_env
from db.redis_connect import r


class Post(StatesGroup):
    topic = State()
    dashboard = State()
    photo = State()
    dashboard_url = State()
    indicators = State()
    date = State()


create_post = Router()
MY_CHANNEL = token_env.my_channel


@create_post.message(F.text == 'Создать пост')
async def start_creating_post(message:Message, state:FSMContext):
    await message.answer('Введите название статьи')
    await state.set_state(Post.topic)


@create_post.message(Post.topic)
async def process_topic(message:Message, state:FSMContext):
    await state.update_data(topic=message.text)
    await state.set_state(Post.dashboard)
    await message.answer("Введи номер дашборда")


@create_post.message(Post.dashboard)
async def process_dashboard(message:Message, state:FSMContext):
    await state.update_data(dashboard=message.text)
    await state.set_state(Post.photo)
    await message.answer("Вставьте фотографию")


@create_post.message(Post.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await state.set_state(Post.dashboard_url)
    await message.answer("Вставьте ссылку на дашборд")


@create_post.message(Post.dashboard_url)
async def process_dashboard_url(message:Message, state:FSMContext):
    await state.update_data(dashboard_url=message.text)
    await state.set_state(Post.indicators)
    await message.answer("Пришлите показатели")


@create_post.message(Post.indicators)
async def proces_indicators_date(message:Message, state:FSMContext):
    number_dashboard = await state.get_data()
    cache = r.get(number_dashboard['dashboard'])
    if cache:
        await state.update_data(indicators=cache, date=date.today())
        await message.answer('Показатели подтянулись')
    else:
        await state.update_data(indicators=message.text, date=date.today())
        r.set(number_dashboard['dashboard'], message.text)
    data = await state.get_data()
    summary = (
        "📢 Новый пост!\n\n"
        "📝 Тема:\n"
        f"{data['topic']}\n\n"
        "📊 Дашборд:\n"
        f"{data['dashboard']}\n"
        f"Ссылка: {data['dashboard_url']}\n\n"
        "📈 Показатели:\n"
        f"{data['indicators']}\n\n"
    )

    db = Session()
    sent_msg = await message.bot.send_photo(chat_id=MY_CHANNEL, photo=data['photo'], caption=summary, parse_mode="Markdown")
    data['message_id'] = sent_msg.message_id
    await CreatePost(db, data)
    await message.answer("Пост успешно создан!")
    db.close()
    await state.clear()






