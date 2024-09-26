from starlette.requests import Request

from app.core.facade import CertificateVendorCore


def get_core(request: Request) -> CertificateVendorCore:
    core: CertificateVendorCore = request.app.state.core
    return core
