from utils.repository import SqlLayer
from models.user_model import UserModel, AddressModel, TokenModel


class UserRepository(SqlLayer):
    model = UserModel


class AddressRepository(SqlLayer):
    model = AddressModel


class TokenRepository(SqlLayer):
    model = TokenModel
