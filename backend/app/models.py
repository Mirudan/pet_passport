from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Enum, Interval, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import date, timedelta
from app.database import Base


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

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    animal_type = Column(String(50))
    birth_date = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="pets")
    weight_history = relationship(
        "WeightRecord",
        back_populates="pet",  # Обратная связь
        order_by="WeightRecord.date.desc()"  # Сортировка по дате (новые сверху)
    )
    procedures = relationship("Procedure", back_populates="pet", cascade="all, delete")

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


class ProcedureType(str, Enum):
    """
    Модель с типами процедур
    """
    VACCINATION = "vaccination"
    PARASITE_TREATMENT = "parasite_treatment"


class Procedure(Base):
    """
    Модель с процедурами
    """
    __tablename__ = "procedures"
    __table_args__ = (
        CheckConstraint("type IN ('vaccination', 'parasite_treatment')", name="valid_procedure_type"),
    )

    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    date_performed = Column(Date, nullable=False, default=date.today())
    validity_days = Column(Integer, nullable=False)
    next_due_date = Column(Date)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="procedures")

    def __init__(self, **kwargs):
        """
        Автоматический расчет следующей даты процедуры (next_due_date)
        :param kwargs: именованные аргументы в виде словаря.
        """
        super().__init__(**kwargs)
        if self.date_performed and self.validity_days:
            self.next_due_date = self.date_performed + timedelta(days=self.validity_days)
