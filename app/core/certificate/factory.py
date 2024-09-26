import time
import uuid
from datetime import datetime

from app.core.certificate.common import Certificate, Status

TIME_FORMAT_FOR_DB = "%Y-%m-%d %H:%M:%S"


class CertificateFactory:
    @classmethod
    def create(
        cls,
        email: str,
        start_date_epoch: float,
        end_date_epoch: float,
        status: Status = Status.ACTIVE,
    ) -> Certificate:
        timestamp = int(time.time() * 1000)
        certificate_key: str = f"{timestamp}-{uuid.uuid4()}"

        # create date
        create_date_epoch = datetime.now().timestamp()
        create_date = datetime.fromtimestamp(create_date_epoch).strftime(
            TIME_FORMAT_FOR_DB
        )

        # start_date
        if start_date_epoch is None:
            start_date = create_date
            start_date_epoch = create_date_epoch
        else:
            start_date = datetime.fromtimestamp(start_date_epoch).strftime(
                TIME_FORMAT_FOR_DB
            )

        end_date = datetime.fromtimestamp(end_date_epoch).strftime(TIME_FORMAT_FOR_DB)

        return Certificate(
            email=email,
            certificate_key=certificate_key,
            status=status,
            create_date=create_date,
            create_date_epoch=create_date_epoch,
            start_date=start_date,
            start_date_epoch=start_date_epoch,
            end_date=end_date,
            end_date_epoch=end_date_epoch,
            delete_date=None,
            delete_date_epoch=None,
        )
