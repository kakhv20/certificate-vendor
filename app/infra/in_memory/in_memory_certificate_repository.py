from collections import defaultdict
from typing import DefaultDict, Optional

from app.core.certificate.interactor import Certificate


class InMemoryCertificateRepository:
    _certificate_table: DefaultDict[tuple[str, str], Certificate]

    def __init__(self) -> None:
        self._certificate_table: DefaultDict[tuple[str, str], Certificate] = defaultdict()

    def create_certificate(self, certificate: Certificate) -> bool:
        email: str = certificate.get_email()
        certificate_key: str = certificate.get_certificate_key()

        for key, value in self._certificate_table.items():
            if key[0] == email and value.get_status() == "ACTIVE":
                return False

        self._certificate_table[(email, certificate_key)] = certificate
        return True

    def check_certificate(self, email: str, certificate_key: str) -> None:
        certificate: Certificate = self._certificate_table.get((email, certificate_key))

        return certificate is not None

    def get_certificate_by_email_and_certificate_key(self, email: str, certificate_key: str) -> Optional[Certificate]:
        return self._certificate_table.get((email, certificate_key))

    def get_active_certificate_by_email(self, email: str) -> Optional[Certificate]:
        for key, value in self._certificate_table.items():
            email_in_db: str = key[0]
            if email_in_db == email and value.get_status() == "ACTIVE":
                return value
        return None

    def get_certificate_by_certificate_key(self, certificate_key: str) -> Optional[Certificate]:
        for key, value in self._certificate_table.items():
            certificate_key_in_db: str = key[1]
            if certificate_key_in_db == certificate_key:
                return value

        return None
