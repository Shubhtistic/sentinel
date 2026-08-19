from uuid_utils import UUID, uuid7

from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    user_id: UUID = Field(default_factory=uuid7, primary_key=True)
    identifier_name: str = Field(unique=True, nullable=False)
    password_hash: str
