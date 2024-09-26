from dataclasses import field
from enum import Enum
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"


class Certificate(Base):
    __tablename__ = "certificates"

    # Primary key field
    certificate_key: str = Column(String, primary_key=True)

    # Other fields
    email: str = Column(String, nullable=False)
    status: str = Column(String, nullable=False)

    # Dates to manage
    create_date: str = Column(String, nullable=False)
    create_date_epoch: float = Column(Float, nullable=False)

    start_date: str = Column(String, nullable=False)
    start_date_epoch: float = Column(Float, nullable=False)

    end_date: str = Column(String, nullable=False)
    end_date_epoch: float = Column(Float, nullable=False)

    delete_date: Optional[str] = Column(String)
    delete_date_epoch: Optional[float] = Column(Float)

    def __init__(
        self,
        certificate_key: str,
        email: str,
        status: Status,
        create_date: str,
        create_date_epoch: float,
        start_date: str,
        start_date_epoch: float,
        end_date: str,
        end_date_epoch: float,
        delete_date: Optional[str] = None,
        delete_date_epoch: Optional[float] = None,
    ) -> None:
        self.certificate_key = certificate_key
        self.email = email
        self.status = status.value
        self.create_date = create_date
        self.create_date_epoch = create_date_epoch
        self.start_date = start_date
        self.start_date_epoch = start_date_epoch
        self.end_date = end_date
        self.end_date_epoch = end_date_epoch
        self.delete_date = delete_date
        self.delete_date_epoch = delete_date_epoch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Certificate):
            return NotImplemented
        return self.certificate_key == other.certificate_key

    def get_email(self) -> str:
        return self.email

    def get_certificate_key(self) -> str:
        return self.certificate_key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "certificate_key": self.certificate_key,
            "email": self.email,
            "status": self.status,
            "create_date": self.create_date,
            "create_date_epoch": self.create_date_epoch,
            "start_date": self.start_date,
            "start_date_epoch": self.start_date_epoch,
            "end_date": self.end_date,
            "end_date_epoch": self.end_date_epoch,
            "delete_date": self.delete_date,
            "delete_date_epoch": self.delete_date_epoch,
        }
