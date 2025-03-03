from app.utils.auth_utils import AuthUtils

class AuthService:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def handle_token(cls, token: str):
        result = AuthUtils.verify_and_refresh_token(token)
        return result