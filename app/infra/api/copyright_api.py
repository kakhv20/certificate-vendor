# `GET /statistics`
#   - Requires pre-set (hard coded) Admin API key
#   - Returns the total number of transactions and platform profit
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.facade import CertificateVendorCore, CreateCertificateResponse, UpdateCopyrightResponse, \
    GetCopyrightResponse, UpdateCopyrightRequest
from app.infra.api.dependables import get_core

copyright_api: APIRouter = APIRouter()

status_translator: Dict[int, Any] = {
    200: {"status_code": status.HTTP_200_OK, "msg": "Copyright retrieved successfully"},
    201: {"status_code": status.HTTP_201_CREATED, "msg": "Copyright created successfully"},
    400: {
        "status_code": status.HTTP_404_NOT_FOUND,
        "msg": "Bad request",
    },
    404: {
        "status_code": status.HTTP_404_NOT_FOUND,
        "msg": "Not found",
    },
}


@copyright_api.post("/copyright", status_code=status.HTTP_201_CREATED)
def update_copyright(
        request: UpdateCopyrightRequest,
        core: CertificateVendorCore = Depends(get_core)
) -> UpdateCopyrightResponse:
    response: UpdateCopyrightResponse = core.update_copyright(request=request)

    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )

    return response


@copyright_api.get("/copyright", status_code=status.HTTP_200_OK)
def get_copyright(
        key: str,
        core: CertificateVendorCore = Depends(get_core)
) -> GetCopyrightResponse:
    response: GetCopyrightResponse = core.get_copyright(key)

    if status_translator[response.status]["status_code"] != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_translator[response.status]["status_code"],
            detail=status_translator[response.status]["msg"],
        )

    return response
