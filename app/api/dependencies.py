from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.services.firebase_service import firebase_service

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Validate Firebase ID token and return current user
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        token = credentials.credentials
        logger.info(f"Attempting authentication with token length: {len(token) if token else 0}")

        # Verify Firebase ID token
        user_data = await firebase_service.verify_user(token)
        if not user_data:
            logger.warning("Token verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = user_data.get("uid")
        if not user_id:
            logger.error("Token verified but no user ID found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Authentication successful for user: {user_id}")
        return {
            "user_id": user_id,
            "email": user_data.get("email")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in authentication: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )

async def get_firebase_service():
    """Get Firebase service instance"""
    return firebase_service