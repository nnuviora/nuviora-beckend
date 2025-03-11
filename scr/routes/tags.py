from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from scr.database.db import get_db
from scr.database.models import User
from scr.schemas import TagModel, TagResponse
from scr.repository import tags as repository_tags
from scr.services.auth import auth_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_tags function returns a list of tags.

    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of tags returned
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :param : Skip the first n tags
    :return: A list of tags
    :doc-author: Trelent
    """
    tags = await repository_tags.get_tags(skip, limit, current_user, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_tag function is used to retrieve a single tag from the database.
    It takes in an integer representing the ID of the tag, and returns a Tag object.


    :param tag_id: int: Specify the tag id
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :param : Get the tag_id from the url
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: TagModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_tag function creates a new tag in the database.

    :param body: TagModel: Pass the data from the request body to the function
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :param : Get the tag id
    :return: A tag object
    :doc-author: Trelent
    """
    print(f"body = {body} \n")
    print(f"db = {db} \n")
    print(f"current_user = {current_user} \n")
    return await repository_tags.create_tag(body, current_user, db)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    body: TagModel,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_tag function updates a tag in the database.
        It takes an id, body and db as parameters. The body is a TagModel object that contains the new values for the tag.
        The function returns an updated TagModel object.

    :param body: TagModel: Pass the body of the request to the function
    :param tag_id: int: Identify the tag to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :param : Get the tag id from the url
    :return: The updated tag, which is the same as the original tag
    :doc-author: Trelent
    """
    tag = await repository_tags.update_tag(tag_id, body, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_tag function removes a tag from the database.

    :param tag_id: int: Pass the tag_id of the tag to be removed
    :param db: Session: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :param : Get the id of the tag to be removed
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.remove_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag

