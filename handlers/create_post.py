from aiogram import Router, F
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import date
from db.CRUD import CreatePost
from db.db_connet import Session


class Post(StatesGroup):
    topic = State()
    dashboard = State()
    dashboard_url = State()
    indicators = State()
    date = State()

create_post = Router()


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
    await state.set_state(Post.dashboard_url)
    await message.answer("Вставьте ссылку на дашборд")


@create_post.message(Post.dashboard_url)
async def process_dashboard_url(message:Message, state:FSMContext):
    await state.update_data(dashboard_url=message.text)
    await state.set_state(Post.indicators)
    await message.answer("Пришлите показатели")


@create_post.message(Post.indicators)
async def proces_indicators_date(message:Message, state:FSMContext):
    await state.update_data(indicators=message.text,date=date.today())
    data = await state.get_data()
    summary = (
        f"Пост готов!\n\n"
        f"Тема: {data['topic']}\n"
        f"Дашборд: {data['dashboard']}\n"
        f"Ссылка: {data['dashboard_url']}\n"
        f"Показатели: {data['indicators']}\n"
        f"Дата: {data['date']}"
    )
    db = Session()
    try:
        CreatePost(db,data)
        await message.answer("Пост успешно создан!")
    except Exception as e:
        print(f"Ошибка {e}")
    finally:
        await message.answer(summary)
        db.close()
    await state.clear()





