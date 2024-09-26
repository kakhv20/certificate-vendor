# `GET /statistics`
#   - Requires pre-set (hard coded) Admin API key
#   - Returns the total number of transactions and platform profit
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import CertificateVendorCore, CreateCertificateResponse, CreateCertificateRequest, \
    CheckCertificateRequest
from app.infra.api.dependables import get_core

certificate_api: APIRouter = APIRouter()

status_translator: Dict[int, Any] = {
    200: {"status_code": status.HTTP_200_OK, "msg": "Action was successful"},
    201: {"status_code": status.HTTP_201_CREATED, "msg": "Certificate created successfully"},
    404: {
        "status_code": status.HTTP_404_NOT_FOUND,
        "msg": "Not found",
    },
}


@certificate_api.post("/certificate", status_code=status.HTTP_201_CREATED)
def create_certificate(
        request: CreateCertificateRequest,
        core: CertificateVendorCore = Depends(get_core)
) -> CreateCertificateResponse:
    response: CreateCertificateResponse = core.create_certificate(request=request)

    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response


@certificate_api.post("/certificate/check", status_code=status.HTTP_200_OK)
def check_certificate(
        request: CheckCertificateRequest,
        core: CertificateVendorCore = Depends(get_core)
) -> None:
    response: Any = core.check_certificate(request=request)

    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )
    return response

# @statistics_api.put("/certificate", status_code=status.HTTP_200_OK)
# def update_certificate(
#         admin_api_key: str, core: CertificateVendorCore = Depends(get_core)
# ) -> None:
#     response: Any = core.create_certificate(admin_api_key=admin_api_key)
#
#     if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
#         raise HTTPException(
#             status_code=status_translator[response.status]["status_code"],
#             detail=status_translator[response.status]["msg"],
#         )
#     return response
