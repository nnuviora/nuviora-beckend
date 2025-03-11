from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from scr.database.models import Note, Tag, User
from scr.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(skip: int, limit: int, user: User, db: Session) -> List[Note]:
    """
    The get_notes function returns a list of notes for the given user.

    :param skip: int: Skip a certain number of notes
    :param limit: int: Limit the number of notes returned
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of notes for a given user
    :doc-author: Also
    """
    return db.query(Note).filter(Note.user_id == user.id).offset(skip).limit(limit).all()


async def get_note(note_id: int, user: User, db: Session) -> Note:
    """
    The get_note function takes in a note_id and user, and returns the Note object with that id.
        If no such note exists, it will return None.

    :param note_id: int: Specify the note id of the note to be returned
    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: The note with the given id for the given user
    :doc-author: Also
    """
    return db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()


async def create_note(body: NoteModel, user: User, db: Session) -> Note:
    """
    The create_note function creates a new note in the database.

    :param body: NoteModel: Get the data from the request body
    :param user: User: Get the user that is logged in
    :param db: Session: Create a database session
    :return: A note object
    :doc-author: Also
    """
    tags = db.query(Tag).filter(and_(Tag.id.in_(body.tags), Tag.user_id == user.id)).all()
    note = Note(title=body.title, description=body.description, tags=tags, user=user)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def remove_note(note_id: int, user: User, db: Session) -> Note | None:
    """
    The remove_note function removes a note from the database.
        Args:
            note_id (int): The id of the note to be removed.
            user (User): The user who owns the note to be removed.
            db (Session): A connection to our database, used for querying and deleting notes.

    :param note_id: int: Specify the note to be deleted
    :param user: User: Identify the user who is requesting to remove a note
    :param db: Session: Pass the database session to the function
    :return: The note that was removed
    :doc-author: Also
    """
    note = db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        db.delete(note)
        db.commit()
    return note


async def update_note(note_id: int, body: NoteUpdate, user: User, db: Session) -> Note | None:
    """
    The update_note function updates a note in the database.
        Args:
            note_id (int): The id of the note to update.
            body (NoteUpdate): The updated information for the Note object.
            user (User): The User object that is making this request, used to verify ownership of this Note object.

    :param note_id: int: Identify the note to be deleted
    :param body: NoteUpdate: Get the data from the request body
    :param user: User: Ensure that the user is logged in
    :param db: Session: Access the database
    :return: The updated note if it exists, otherwise none
    :doc-author: Also
    """
    note = db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        tags = db.query(Tag).filter(and_(Tag.id.in_(body.tags), Note.user_id == user.id)).all()
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        db.commit()
    return note


async def update_status_note(note_id: int, body: NoteStatusUpdate, user: User, db: Session) -> Note | None:
    """
    The update_status_note function updates the status of a note in the database.

    :param note_id: int: Find the note in the database
    :param body: NoteStatusUpdate: Get the done parameter from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A note object or none if the note does not exist
    :doc-author: Also
    """
    note = db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        note.done = body.done
        db.commit()
    return note
