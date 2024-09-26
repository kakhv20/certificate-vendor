import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.facade import CertificateVendorCore
from app.infra.api.certificate_api import certificate_api
from app.infra.api.copyright_api import copyright_api
from app.infra.email_sender.SMTP import SMTPEmailSender
from app.infra.in_memory.in_memory_certificate_repository import (
    InMemoryCertificateRepository,
)
from app.infra.in_memory.in_memory_copyright_repository import (
    InMemoryCopyrightRepository,
)
from app.infra.postgreSQL.postgres_certificate_repository import (
    PostgresCertificateRepository,
)
from app.infra.postgreSQL.postgres_copyright_repository import (
    PostgresCopyrightRepository,
)

# Global SQLAlchemy setup


def setup(use_real_db: bool) -> FastAPI:
    def init_fast_api() -> FastAPI:
        fast_api: FastAPI = FastAPI()
        fast_api.include_router(certificate_api)
        fast_api.include_router(copyright_api)
        return fast_api

    def init_repositories() -> dict:
        # Create a new session for repository initialization
        session = session_local()
        try:
            return {
                "certificate_repository": PostgresCertificateRepository(session),
                "copyright_repository": PostgresCopyrightRepository(session),
            }
        finally:
            session.close()  # Ensure the session is closed

    def init_in_memory_dbs() -> dict:
        return {
            "certificate_repository": InMemoryCertificateRepository(),
            "copyright_repository": InMemoryCopyrightRepository(),
        }

    def initialize_smtp():
        smtp_settings = {
            "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
            "port": int(os.getenv("SMTP_PORT", 587)),  # Convert to int
            "username": os.getenv("SMTP_USERNAME", "info@ucraft.io"),
            "password": os.getenv("SMTP_PASSWORD", "zuuz ckrm hwdt krxj"),
        }
        return SMTPEmailSender.create(**smtp_settings)

    app = init_fast_api()

    # Choose the repository based on the use_real_db flag
    if use_real_db:
        sqlalchemy_database_url = os.getenv(
            "db_url",
            os.getenv(
                "db_url",
                "postgresql://admin:admin@localhost:5432/certificate_vendor_db",
            ),
        )
        engine = create_engine(sqlalchemy_database_url)
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_initializer = init_repositories
    else:
        db_initializer = init_in_memory_dbs

    app.state.core = CertificateVendorCore.create(
        **db_initializer(), email_sender=initialize_smtp()
    )

    return app
