from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
  prefix='/posts',
  tags=['Posts']
)

# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
  # cursor.execute("""SELECT * FROM posts """)
  # posts = cursor.fetchall()
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  return posts

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""select * from posts where id = %s """, (str(id)))
  # post = cursor.fetchone()
  # post = db.query(models.Post).filter(models.Post.id == id).first()
  post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the ID {id} was not found")
  return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
  # new_post = cursor.fetchone()
  # conn.commit()
  # new_post = models.Post(title=post.title, content=post.content, published=post.published)
  # new_post = models.Post(**post.dict())
  new_post = models.Post(owner_id = current_user.id, **post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""", (post.title, post.content, post.published, str(id)))
  # upated_post = cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to preform requested action')
  post_query.update(updated_post.model_dump(), synchronize_session=False)
  db.commit()
  return post_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
  # cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
  # deleted_post = cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to preform requested action')
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)