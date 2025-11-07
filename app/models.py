from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, TIMESTAMP ,Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql.expression import text


Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  = mapped_column(String(30))
    # username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    notes = relationship('Note')
    
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("now()"),  onupdate=text("now()"))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")