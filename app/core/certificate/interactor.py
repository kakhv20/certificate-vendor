from typing import Protocol, Dict, Any, Optional
from dataclasses import dataclass

from app.core.certificate.common import Certificate
from app.core.certificate.factory import CertificateFactory


class ICertificateRepository(Protocol):

    def create_certificate(self, certificate: Certificate) -> bool:
        pass

    def check_certificate(self, email: str, certificate_key: str) -> None:
        pass

    def get_certificate_by_email_and_certificate_key(self, email: str, certificate_key: str) -> Optional[Certificate]:
        pass

    def get_active_certificate_by_email(self, email: str) -> Optional[Certificate]:
        pass

    def get_certificate_by_certificate_key(self, email: str, certificate_key: str) -> Optional[Certificate]:
        pass


@dataclass
class CertificateInteractor:
    _certificate_repository: ICertificateRepository

    def create_certificate(self, email: str, start_date: float, end_date: float) -> Certificate:
        new_certificate: Certificate = CertificateFactory.create(email, start_date, end_date)
        self._certificate_repository.create_certificate(new_certificate)

        return new_certificate

    def check_certificate(self, email: str, certificate_key: str):
        return self._certificate_repository.check_certificate(email, certificate_key)
