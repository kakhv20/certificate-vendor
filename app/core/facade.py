from dataclasses import dataclass
from typing import Protocol

from app.core.certificate.common import Certificate
from app.core.certificate.interactor import CertificateInteractor, ICertificateRepository
from app.core.copyright.interactor import CopyrightInteractor, ICopyrightRepository


@dataclass
class CreateCertificateRequest:
    email: str
    start_date: float
    end_date: float


@dataclass
class CreateCertificateResponse:
    status: int


@dataclass
class CheckCertificateRequest:
    email: str
    certificate_key: str


@dataclass
class CheckCertificateResponse:
    status: int
    certificate_key_is_valid: bool


@dataclass
class UpdateCopyrightRequest:
    key: str
    subject: str
    copyright_txt: str


@dataclass
class UpdateCopyrightResponse:
    status: int


@dataclass
class GetCopyrightResponse:
    status: int
    subject: str
    copyright_text: str


class IEmailSender(Protocol):
    def send_email(self, to_email: str, subject: str, copyright_txt: str, certificate_key: str) -> None:
        pass


@dataclass
class CertificateVendorCore:
    _certificate_interactor: CertificateInteractor
    _copyright_interactor: CopyrightInteractor
    _email_sender: IEmailSender

    @classmethod
    def create(
            cls,
            certificate_repository: ICertificateRepository,
            copyright_repository: ICopyrightRepository,
            email_sender: IEmailSender
    ):
        return cls(
            _certificate_interactor=CertificateInteractor(_certificate_repository=certificate_repository),
            _copyright_interactor=CopyrightInteractor(_copyright_repository=copyright_repository),
            _email_sender=email_sender
        )

    def create_certificate(
            self, request: CreateCertificateRequest
    ) -> CreateCertificateResponse:
        print("Creating certificate")
        certificate: Certificate = self._certificate_interactor.create_certificate(request.email, request.start_date,
                                                                                   request.end_date)
        print(certificate)

        if certificate:
            status: int = 201
            self.send_notification(email=request.email, certificate_key=certificate.get_certificate_key())
        else:
            status: int = 400

        return CreateCertificateResponse(status)

    def send_notification(self, email: str, certificate_key: str):
        print("Sending email")
        copyright_object: dict = self._copyright_interactor.get_copy_for_key("email")

        self._email_sender.send_email(
            to_email=email,
            subject=copyright_object['subject'],
            copyright_txt=copyright_object['copyright_txt'],
            certificate_key=certificate_key
        )

    def check_certificate(self, request: CheckCertificateRequest):
        print("checking email {} certificate_key {} combination", request.email, request.certificate_key)
        is_valid: bool = self._certificate_interactor.check_certificate(
            email=request.email,
            certificate_key=request.certificate_key
        )
        print("result: {}", is_valid)
        if is_valid:
            status: int = 200
        else:
            status: int = 400

        return CheckCertificateResponse(status, is_valid)

    def update_copyright(self, request: UpdateCopyrightRequest) -> UpdateCopyrightResponse:
        key, subject, copyright_txt = request.key, request.subject, request.copyright_txt

        print("Updating copyright. Key: {}, subject {}", key, subject)
        print("Text {}", copyright_txt)
        self._copyright_interactor.update_copyright(key=key, subject=subject, copyright_txt=copyright_txt)

        return UpdateCopyrightResponse(200)

    def get_copyright(self, key: str) -> GetCopyrightResponse:
        print("Get copyright")
        copyright_object: dict = self._copyright_interactor.get_copy_for_key(key=key)
        print("Copyright object: {}", copyright_object)

        if copyright_object:
            status: int = 200
        else:
            status: int = 400

        return GetCopyrightResponse(
            status=status,
            subject=copyright_object['subject'],
            copyright_text=copyright_object['copyright_text']
        )
