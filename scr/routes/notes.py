from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from scr.database.db import get_db
from scr.database.models import User
from scr.schemas import NoteModel, NoteUpdate, NoteStatusUpdate, NoteResponse
from scr.repository import notes as repository_notes
from scr.services.auth import auth_service


router = APIRouter(prefix='/notes', tags=["notes"])


# @router.get("/", response_model=List[NoteResponse])
# async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
#                      current_user: User = Depends(auth_service.get_current_user)):
#     notes = await repository_notes.get_notes(skip, limit, current_user, db)
#     return notes
@router.get("/", response_model=List[NoteResponse], description='No more than 2 requests per 5 sec',
            dependencies=[Depends(RateLimiter(times=2, seconds=10))])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_notes function is a GET request that returns all notes in the database.
    It takes three optional parameters: skip, limit, and db. The skip parameter allows you to specify how many notes to skip
    before returning results (defaults to 0). The limit parameter allows you to specify how many results should be returned
    (defaults 100). Finally, the db parameter is used by FastAPI's dependency injection system for accessing the database.

    :param skip: int: Skip the first n notes
    :param limit: int: Limit the number of notes returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of notes, which is the same as the note model
    :doc-author: Trelent
    """

    notes = await repository_notes.get_notes(skip, limit, current_user, db)
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_note function is used to retrieve a single note from the database.
    It takes in an integer ID and returns a Note object.


    :param note_id: int: Specify the note id that will be used to retrieve a specific note
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A note object
    :doc-author: Trelent
    """

    note = await repository_notes.get_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
        body: NoteModel,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_note function creates a new note in the database.

    :param body: NoteModel: Pass the data to create a note
    :param db: Session: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :param : Get the note id from the url
    :return: A note object, which is the same as the body
    :doc-author: Trelent
    """

    # print(f"body = {body} \n")
    # print(f"db = {db} \n")
    # print(f"current_user = {current_user} \n")
    return await repository_notes.create_note(body, current_user, db)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(body: NoteUpdate, note_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_note function updates a note in the database.

    :param body: NoteUpdate: Get the data from the request body
    :param note_id: int: Get the note id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the user who is currently logged in
    :return: A note object
    :doc-author: Trelent
    """

    note = await repository_notes.update_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_status_note(body: NoteStatusUpdate, note_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_status_note function updates the status of a note.
        The function takes in a NoteStatusUpdate object, which contains the new status for the note.
        It also takes in an integer representing the id of the note to be updated and two optional parameters:
            - db: A database session that is used to query data from our database (defaults to Depends(get_db))
            - current_user: An instance of User containing information about our currently logged-in user (defaults to Depends(auth_service.get_current_user))

    :param body: NoteStatusUpdate: Get the status of the note
    :param note_id: int: Get the note id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A note object with the updated status
    :doc-author: Trelent
    """

    note = await repository_notes.update_status_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def remove_note(note_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_note function removes a note from the database.

    :param note_id: int: Specify the note to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A note object
    :doc-author: Trelent
    """

    note = await repository_notes.remove_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note
