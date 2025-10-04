from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db.CRUD import all_post, delete_post
from db.db_connet import Session
from service import token_env

del_post = Router()
MY_CHANNEL = token_env.my_channel


class DeletePostStates(StatesGroup):
    choosing_post = State()
    confirming = State()


@del_post.message(F.text == 'Удалить пост')
async def start_deleting_post(message: Message, state: FSMContext):
    db = Session()
    posts = await all_post(db, 5)
    db.close()

    if not posts:
        await message.answer("Постов нет")
        return

    await state.update_data(posts=[(post.id, post.topic) for post in posts])
    await state.set_state(DeletePostStates.choosing_post)

    text = "Выберите пост для удаления:\n"

    for post in posts:
        text += f"{post.id} — {post.topic}\n"
    await message.answer(text)


@del_post.message(DeletePostStates.choosing_post)
async def choose_post(message: Message, state: FSMContext):
    data = await state.get_data()
    posts = dict(data['posts'])

    try:
        post_id = int(message.text)
    except ValueError:
        await message.answer("Введите корректный ID поста")
        return

    if post_id not in posts:
        await message.answer("Такого поста нет в списке")
        return

    await state.update_data(selected_post_id=post_id)
    await state.set_state(DeletePostStates.confirming)
    await message.answer(f"Вы уверены, что хотите удалить пост '{posts[post_id]}'? (да/нет)")


@del_post.message(DeletePostStates.confirming)
async def confirm_delete(message: Message, state: FSMContext):
    text = message.text.lower()
    data = await state.get_data()
    post_id = data['selected_post_id']

    if text == 'да':
        db = Session()
        await delete_post(db, message.bot, post_id, MY_CHANNEL)
        db.close()
        await message.answer("Пост удалён")
    else:
        await message.answer("Удаление отменено")

    await state.clear()








