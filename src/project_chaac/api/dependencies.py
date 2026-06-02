from fastapi import Header, HTTPException, Request, status

from project_chaac.config import settings


async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """Mock API key check.

    Real version: look x_api_key up in the partner registry instead of
    comparing to a single configured value.
    """
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key


async def verify_client_ip(request: Request) -> None:
    """Mock IP allowlist gate.

    NOTE: behind an ingress/proxy this sees the proxy IP, not the real client.
    On K8s you'll need to read X-Forwarded-For instead. Fine while mocked.
    """
    allowed = {ip.strip() for ip in settings.allowed_ips.split(",")}
    client_host = request.client.host if request.client else None
    print(f"Client IP: {client_host}, Allowed IPs: {allowed}")
    if client_host not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client IP not allowed",
        )