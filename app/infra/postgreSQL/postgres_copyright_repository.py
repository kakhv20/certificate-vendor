from sqlalchemy import MetaData, Table, String, Text, Column
from sqlalchemy.orm import Session
from typing import Optional
from app.models.copyright import Copyright


class PostgresCopyrightRepository:
    def __init__(self, session: Session) -> None:
        """
        Initialize with an active SQLAlchemy session.
        :param session: SQLAlchemy session to interact with the PostgreSQL database.
        """
        self.session = session
        metadata = MetaData()

        # Define the copyrights table
        self.copyrights_table = Table(
            "copyrights",
            metadata,
            Column("key", String, primary_key=True),
            Column("subject", String),
            Column("copyright_txt", Text),
        )

        # Create the table in the database (if it doesn't exist)
        metadata.create_all(self.session.get_bind())

    def update_copyright(self, key: str, subject: str, copyright_txt: str) -> None:
        # Check if the copyright for the key already exists
        existing_copyright = self.session.query(Copyright).filter_by(key=key).first()

        if existing_copyright:
            # Update the existing record
            existing_copyright.subject = subject
            existing_copyright.copyright_txt = copyright_txt
        else:
            # Create a new copyright entry
            new_copyright = Copyright(
                key=key, subject=subject, copyright_txt=copyright_txt
            )
            self.session.add(new_copyright)

        # Commit the transaction
        self.session.commit()

    def get_copy_for_key(self, key: str) -> Optional[dict]:
        # Query the copyright by key
        copyright_record = self.session.query(Copyright).filter_by(key=key).first()

        # Return the data as a dictionary if it exists
        if copyright_record:
            return {
                "subject": copyright_record.subject,
                "copyright_txt": copyright_record.copyright_txt,
            }
        return None
