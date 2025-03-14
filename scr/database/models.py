
import enum

from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    tags = relationship("Tag", secondary=note_m2m_tag, backref="notes")
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="notes")


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='unique_tag_user'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="tags")
    # Використовуємо overlaps для уникнення конфлікту
    images = relationship("Image", secondary="note_m2m_tag", overlaps="notes,tags")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(255), nullable=False)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    owner_id = Column('owner_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    owner = relationship("User", backref="comments")
    image = relationship("Image", backref="comments")


class Role(enum.Enum):
    user: str = "user"
    moderator: str = "moderator"
    admin: str = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column("role", Enum(Role), default=Role.user)
    active = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False, nullable=True)


class Role(enum.Enum):
    user: str = "user"
    moderator: str = "moderator"
    admin: str = "admin"

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    owner_id = Column('owner_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    url_original = Column(String(255), nullable=False)
    url_transformed = Column(String(255), nullable=True)
    url_original_qr = Column(String(255), nullable=False)
    url_transformed_qr = Column(String(255), nullable=True)
    tags = relationship("Tag", secondary=note_m2m_tag, backref="images")
    description = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime)
    owner = relationship("User", backref="images")
    # Використовуємо overlaps для уникнення конфлікту
    tags = relationship("Tag", secondary="note_m2m_tag", overlaps="notes,tags")

    def json(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "url_original": self.url_original,
            "url_transformed": self.url_transformed,
            "url_original_qr": self.url_original_qr,
            "url_transformed_qr": self.url_transformed_qr,
            "tags": [tag.name for tag in self.tags],
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
        }
