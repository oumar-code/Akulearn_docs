"""Dependency providers for Aku-IGHub."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer(auto_error=False)


def _decode_roles(token: str) -> list[str]:
    """Placeholder parser until JWT validation is wired to a real auth provider."""
    if token.startswith("role:"):
        raw_roles = token.split(":", 1)[1]
        return [r.strip() for r in raw_roles.split(",") if r.strip()]
    return ["operator"]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, object]:
    """Return an authenticated principal shape used by routers.

    This keeps scaffolds runnable in CI while preserving an auth integration seam.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token is required.",
        )

    roles = _decode_roles(credentials.credentials)
    return {
        "sub": "scaffold-user",
        "roles": roles,
        "scopes": ["ig:read", "ig:write"],
        "token": credentials.credentials,
    }


def require_roles(*required_roles: str):
    required = set(required_roles)

    async def _checker(user: dict[str, object] = Depends(get_current_user)) -> dict[str, object]:
        roles = set(user.get("roles", []))
        if required and roles.isdisjoint(required):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {sorted(required)}",
            )
        return user

    return _checker
