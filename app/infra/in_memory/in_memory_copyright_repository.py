from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class InMemoryCopyrightRepository:
    _copyright_values: dict = field(default_factory=lambda: defaultdict(dict))

    def update_copyright(self, key: str, subject: str, copyright_txt: str) -> None:
        self._copyright_values[key] = {"subject": subject, "copyright_txt": copyright_txt}

    def get_copy_for_key(self, key: str) -> dict:
        return self._copyright_values[key]
