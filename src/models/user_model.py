import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, primary_key=True, unique=True, index=True
    )
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    birth_date: Mapped[datetime] = mapped_column(default=datetime.now())
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    is_activate: Mapped[bool] = mapped_column(default=False)
    is_locked: Mapped[bool] = mapped_column(default=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))

    hash_password: Mapped[str] = mapped_column()

    role: Mapped["RoleModel"] = relationship(back_populates="user")
    token: Mapped["TokenModel"] = relationship(back_populates="user")
    address: Mapped["AddressModel"] = relationship(back_populates="user")

    async def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "phone": self.phone,
            "birth_date": self.birth_date,
            "created_at": self.created_at,
            "update_at": self.updated_at,
            "is_activate": self.is_activate,
            "is_locked": self.is_locked,
        }


class AddressModel(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    address_line: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()  # Warning
    state: Mapped[str] = mapped_column()
    postal_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()  # Warning
    is_default: Mapped[bool] = mapped_column(default=False)

    user: Mapped["UserModel"] = relationship(back_populates="address")


class TokenModel(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    refresh_token: Mapped[str] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column()
    user_agent: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user: Mapped["UserModel"] = relationship(back_populates="token")


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    role: Mapped[str] = mapped_column()

    user: Mapped["UserModel"] = relationship(back_populates="role")

    async def to_dict(self):
        pass
