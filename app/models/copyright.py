from dataclasses import dataclass
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class Copyright(Base):
    __tablename__ = "copyrights"

    key: str = Column(String, primary_key=True)
    subject: str = Column(String)
    copyright_txt: str = Column(Text)

    def __init__(self, key: str, subject: str, copyright_txt: str) -> None:
        self.key = key
        self.subject = subject
        self.copyright_txt = copyright_txt
