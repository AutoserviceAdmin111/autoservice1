import hashlib
import secrets
from base64 import urlsafe_b64encode
from social_core.backends.oauth import BaseOAuth2

class KeycloakPKCEBackend(BaseOAuth2):
    name = 'keycloak'
    AUTHORIZATION_URL = 'http://localhost:8080/realms/automaster/protocol/openid-connect/auth'
    ACCESS_TOKEN_URL = 'http://localhost:8080/realms/automaster/protocol/openid-connect/token'
    USERINFO_URL = 'http://localhost:8080/realms/automaster/protocol/openid-connect/userinfo'
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['openid', 'profile', 'email', 'phone', 'roles']
    EXTRA_DATA = [('refresh_token', 'refresh_token'), ('expires_in', 'expires')]

    def generate_code_verifier(self):
        return secrets.token_urlsafe(64)

    def generate_code_challenge(self, code_verifier):
        digest = hashlib.sha256(code_verifier.encode()).digest()
        return urlsafe_b64encode(digest).decode().replace('=', '')

    def auth_params(self, state=None):
        params = super().auth_params(state)
        code_verifier = self.generate_code_verifier()
        self.strategy.session_set('code_verifier', code_verifier)
        params.update({
            'code_challenge': self.generate_code_challenge(code_verifier),
            'code_challenge_method': 'S256'
        })
        return params

    def request_access_token(self, *args, **kwargs):
        kwargs['data']['client_id'] = self.setting('KEY')
        kwargs['data']['client_secret'] = self.setting('SECRET')
        kwargs['data']['code_verifier'] = self.strategy.session_get('code_verifier')
        return super().request_access_token(*args, **kwargs)

    def get_user_details(self, response):
        # Обработка данных пользователя из Keycloak
        return {
            'username': response.get('preferred_username'),
            'email': response.get('email', ''),
            'first_name': response.get('given_name', ''),
            'last_name': response.get('family_name', '')
        }

    def user_data(self, access_token, *args, **kwargs):
        # Получение данных пользователя через UserInfo endpoint
        return self.get_json(
            self.USERINFO_URL,
            headers={'Authorization': f'Bearer {access_token}'}
        )
