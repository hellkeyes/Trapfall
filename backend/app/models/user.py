from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)   

    password_hash: Mapped[str] = mapped_column()