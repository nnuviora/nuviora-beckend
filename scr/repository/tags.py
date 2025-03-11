from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from scr.database.models import Tag, User
from scr.schemas import TagModel


async def get_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
    """
    The get_tags function returns a list of tags for the given user.

    :param skip: int: Set the number of records to skip
    :param limit: int: Limit the number of tags returned
    :param user: User: Filter the tags by user
    :param db: Session: Pass the database session to the function
    :return: A list of tags
    :doc-author: Trelent
    """
    return db.query(Tag).filter(Tag.user_id == user.id).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, user: User, db: Session) -> Tag:
    """
    The get_tag function takes in a tag_id and user, and returns the Tag object with that id.
    If no such tag exists, it raises an HTTPException.

    :param tag_id: int: Specify the tag id
    :param user: User: Get the user that is making the request
    :param db: Session: Access the database
    :return: A tag object if it exists, otherwise it returns none
    :doc-author: Trelent
    """
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()


async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.

    :param body: TagModel: Get the name of the tag from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The newly created tag
    :doc-author: Trelent
    """
    tag = Tag(name=body.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, user: User, db: Session) -> Tag | None:
    """
    The update_tag function updates a tag in the database.
        Args:
            tag_id (int): The id of the tag to update.
            body (TagModel): The updated TagModel object with new values for name and color.
            user (User): The current logged-in user, used to verify that they are authorized to update this item.

    :param tag_id: int: Find the tag in the database
    :param body: TagModel: Pass the new tag name
    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: A tag object
    :doc-author: Trelent
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        tag .name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: User, db: Session) -> Tag | None:
    """
    The remove_tag function removes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be removed.
            user (User): The user who owns the tags being removed.
            db (Session): A connection to our database, used for querying and deleting data.

    :param tag_id: int: Specify the id of the tag to remove
    :param user: User: Ensure that the user is authorized to delete the tag
    :param db: Session: Pass the database session to the function
    :return: The tag that was removed
    :doc-author: Trelent
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
