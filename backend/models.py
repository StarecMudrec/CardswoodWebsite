from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Numeric, DateTime, JSON, String, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AllowedUser(Base):
    __tablename__ = "allowed_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)


class AuthToken(Base):
    __tablename__ = "auth_token"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    def __repr__(self):
        return f"<AuthToken token={self.token} user_id={self.user_id}>"


class Season(Base):
    __tablename__ = "season"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def present(self):
        return {"id": self.id, "uuid": self.uuid, "name": self.name}


class Card(Base):
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    img: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    season_id: Mapped[int] = mapped_column(Integer, ForeignKey("season.id", ondelete="CASCADE"), nullable=False)

    season = relationship("Season", backref="cards")
    comments = relationship("Comment", lazy="selectin", cascade="all, delete-orphan", back_populates="card")

    def present(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "season_id": self.season_id,
            "img": self.img,
            "category": self.category,
            "name": self.name,
            "description": self.description,
        }


class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("card.id", ondelete="CASCADE"), nullable=False)

    card = relationship("Card", back_populates="comments")

    def present(self):
        return {"id": self.id, "uuid": self.uuid, "user_id": self.user_id, "text": self.text, "card_id": self.card_id}


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    items: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    payanyway_payment_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    notification_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default="pending")
    notification_error: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.order_number} status={self.status}>"
