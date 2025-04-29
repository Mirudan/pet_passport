from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String(255))
    username = Column(String(50))
    role = Column(String(20), default="user")
    pets = relationship(
        "Pet",
        back_populates="owner",
        cascade="all, delete"
    )
    preferred_weight_unit = Column(String(1), default='g')


class Pet(Base):
    """
    Модель питомца
    """
    __tablename__ = "pets"

    name = Column(String(100), nullable=False)
    animal_type = Column(String(50))
    birth_date = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight_history = relationship(
        "WeightRecord",
        back_populates="pet",  # Обратная связь
        order_by="WeightRecord.date.desc()"  # Сортировка по дате (новые сверху)
    )

    @property
    def last_weights(self):
        """
        Свойство для получения последних 5 записей веса
        :return: список из 5 первых элементов.
        """
        return self.weight_history[:5]


class WeightRecord(Base):
    """
    Модель записи веса
    """
    __tablename__ = "weight_records"

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    unit = Column(String(1), default='g')
    pet = relationship("Pet", back_populates="weight_history")
