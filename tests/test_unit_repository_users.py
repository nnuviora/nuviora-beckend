import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from scr.database.models import Note, Tag, User
from scr.schemas import UserModel, UserDb, TokenModel, RequestEmail
from scr.repository.users import (
    create_user,
    update_token,
    update_avatar_url,
    confirmed_email,
    get_user_by_email,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_not_get_user_by_email(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(self.user.email, db=self.session)
        self.assertIsNone(result)

    # async def test_get_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await get_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username="test_user", email="test@mail.com", password="test_pass")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    # async def test_remove_note_found(self):
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_remove_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)

    async def test_update_token_found(self):
        token_new = "test_token"
        self.session.commit.return_value = None
        result = await update_token(user=self.user, token=token_new, db=self.session)
        self.assertEqual(result, None)

    # async def test_update_note_not_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)
    #
    async def test_confirmed_email_found(self):
        user_email = User.email
        # self.session.commit.return_value = None
        result = await confirmed_email(user_email, db=self.session)
        self.assertIsNone(result)

    async def test_update_avatar_url_found(self):
        user_email = User.email
        avatar_url = "test_update_avatar_url"
        result = await update_avatar_url(user_email, avatar_url, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
