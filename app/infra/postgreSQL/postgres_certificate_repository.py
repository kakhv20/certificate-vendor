from sqlalchemy.orm import Session
from sqlalchemy import and_, MetaData, Table, Column, String, Float
from typing import Optional

from app.core.certificate.common import Certificate, Status


class PostgresCertificateRepository:
    def __init__(self, session: Session) -> None:
        """
        Initialize with an active SQLAlchemy session.
        :param session: SQLAlchemy session to interact with the PostgreSQL database.
        """
        self.session = session
        metadata = MetaData()

        # Define the certificates table
        self.certificates_table = Table(
            "certificates",
            metadata,
            Column("certificate_key", String, primary_key=True),
            Column("email", String, nullable=False),
            Column("status", String, nullable=False),
            Column("create_date", String, nullable=False),
            Column("create_date_epoch", Float, nullable=False),
            Column("start_date", String, nullable=False),
            Column("start_date_epoch", Float, nullable=False),
            Column("end_date", String, nullable=False),
            Column("end_date_epoch", Float, nullable=False),
            Column("delete_date", String),
            Column("delete_date_epoch", Float),
        )

        # Create the table in the database (if it doesn't exist)
        metadata.create_all(self.session.get_bind())

    def create_certificate(self, certificate: Certificate) -> bool:
        email: str = certificate.get_email()
        certificate_key: str = certificate.get_certificate_key()

        # Check if an active certificate exists for the email
        existing_certificate = (
            self.session.query(Certificate)
            .filter(
                and_(
                    Certificate.email == email,
                    Certificate.status == Status.ACTIVE.value,
                )
            )
            .first()
        )

        if existing_certificate:
            return False

        # Add the new certificate
        self.session.add(certificate)
        self.session.commit()

        return True

    def check_certificate(self, email: str, certificate_key: str) -> bool:
        certificate = (
            self.session.query(Certificate)
            .filter(
                and_(
                    Certificate.email == email,
                    Certificate.certificate_key == certificate_key,
                )
            )
            .first()
        )

        return certificate is not None

    def get_certificate_by_email_and_certificate_key(
        self, email: str, certificate_key: str
    ) -> Optional[Certificate]:
        return (
            self.session.query(Certificate)
            .filter(
                and_(
                    Certificate.email == email,
                    Certificate.certificate_key == certificate_key,
                )
            )
            .first()
        )

    def get_active_certificate_by_email(self, email: str) -> Optional[Certificate]:
        return (
            self.session.query(Certificate)
            .filter(
                and_(Certificate.email == email, Certificate.status == Status.ACTIVE)
            )
            .first()
        )

    def get_certificate_by_certificate_key(
        self, certificate_key: str
    ) -> Optional[Certificate]:
        return (
            self.session.query(Certificate)
            .filter(and_(Certificate.certificate_key == certificate_key, True))
            .first()
        )
