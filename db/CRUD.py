from db.models import Post
from sqlalchemy.orm import Session


async def CreatePost(db: Session,post_data):
    new_post = Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


async def delete_post(db, bot, post_id, chanel_id):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False

    try:
        await bot.delete_message(chat_id=chanel_id, message_id=post.message_id)
    except Exception as e:
        print(f"Не удалось удалить сообщение из канала: {e}")

    db.delete(post)
    db.commit()
    return True


async def all_post(db: Session, num_post):
    return db.query(Post).order_by(Post.id.desc()).limit(num_post).all()




