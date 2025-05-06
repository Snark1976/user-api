from advanced_alchemy.extensions.litestar import base
from sqlalchemy import Column, String

class User(base.UUIDAuditBase):
    __tablename__ = "user"

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)