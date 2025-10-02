from db.models import Post
from sqlalchemy.orm import Session


def CreatePost(db: Session,post_data):
    new_post = Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

