import os
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer()

def validate_token( credentials: HTTPAuthorizationCredentials = Depends(bearer),):
    print('performing token validation')
    expected_token = os.getenv("API_ACCESS_TOKEN")

    if not expected_token:
        raise HTTPException(status_code=500,detail="API_ACCESS_TOKEN is not configured",)

    if not secrets.compare_digest(credentials.credentials, expected_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid bearer token",)

    return credentials.credentials