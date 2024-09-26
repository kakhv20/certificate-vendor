from dataclasses import dataclass
from typing import Protocol


class ICopyrightRepository(Protocol):
    def update_copyright(self, key: str, subject: str, copyright_txt: str) -> None:
        pass

    def get_copy_for_key(self, key: str) -> dict:
        pass


@dataclass
class CopyrightInteractor:
    _copyright_repository: ICopyrightRepository

    def update_copyright(self, key: str, subject: str, copyright_txt: str) -> None:
        self._copyright_repository.update_copyright(key=key, subject=subject, copyright_txt=copyright_txt)

    def get_copy_for_key(self, key: str) -> dict:
        copy_text: dict = self._copyright_repository.get_copy_for_key(key=key)

        if copy_text:
            return copy_text

        raise Exception("Copy for this key does not exist")
