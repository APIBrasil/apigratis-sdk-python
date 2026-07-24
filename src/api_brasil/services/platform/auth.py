"""Autenticação e conta."""

from __future__ import annotations

from typing import Any, Mapping, Optional

from ...core.http import HttpClient
from ...core.types import Json

__all__ = ["AuthService"]


class AuthService:
    """Autenticação e conta (``/auth/*``, ``/profile*``, ``/password/*``).

    :meth:`login` e :meth:`verify_2fa` guardam automaticamente o Bearer Token
    retornado no cliente, deixando as próximas chamadas autenticadas.
    """

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def login(self, body: Json, **options: Any) -> Any:
        """Autentica com email/senha: ``POST /auth/login``.

        Se a conta tiver 2FA, retorna ``{"requires_2fa": True, "challenge": ...}``
        — use :meth:`send_2fa` + :meth:`verify_2fa` para concluir.

        :param body: ``email``, ``password``, ``turnstile_token``
        """
        response = self.http.post("/auth/login", body, **options)
        self._store_token(response)

        return response

    def send_2fa(self, body: Json, **options: Any) -> Any:
        """Envia o código 2FA pelo método escolhido: ``POST /auth/2fa/send``.

        :param body: ``challenge``, ``method`` (email|sms|whatsapp|call)
        """
        return self.http.post("/auth/2fa/send", body, **options)

    def verify_2fa(self, body: Json, **options: Any) -> Any:
        """Conclui o login com o código 2FA: ``POST /auth/login/verify-2fa``.

        :param body: ``challenge``, ``code``
        """
        response = self.http.post("/auth/login/verify-2fa", body, **options)
        self._store_token(response)

        return response

    def two_factor_methods(self, **options: Any) -> Any:
        """Lista os métodos 2FA ativos da conta: ``GET /auth/2fa/methods``."""
        return self.http.get("/auth/2fa/methods", **options)

    def register(self, body: Json, **options: Any) -> Any:
        """Cria uma conta: ``POST /auth/register``.

        :param body: ``first_name``, ``email``, ``cellphone``, ``password``,
            ``terms_accepted``
        """
        return self.http.post("/auth/register", body, **options)

    def register_simple(self, body: Json, **options: Any) -> Any:
        """Cadastro simplificado: ``POST /auth/register/simple``."""
        return self.http.post("/auth/register/simple", body, **options)

    def verification_send(self, body: Json, **options: Any) -> Any:
        """Dispara verificação de email/celular: ``POST /auth/verification/send``.

        :param body: ``type`` (email|cellphone)
        """
        return self.http.post("/auth/verification/send", body, **options)

    def verification_verify(self, body: Json, **options: Any) -> Any:
        """Confirma o código de verificação: ``POST /auth/verification/verify``.

        :param body: ``code``, ``type``
        """
        return self.http.post("/auth/verification/verify", body, **options)

    def password_forgot(self, body: Json, **options: Any) -> Any:
        """Esqueci a senha: ``POST /auth/password/forgot``.

        :param body: ``identifier``, ``method`` (email|sms|whatsapp)
        """
        return self.http.post("/auth/password/forgot", body, **options)

    def password_verify_code(self, body: Json, **options: Any) -> Any:
        """Valida o código de recuperação: ``POST /auth/password/verify-code``.

        :param body: ``identifier``, ``code``
        """
        return self.http.post("/auth/password/verify-code", body, **options)

    def password_reset(self, body: Json, **options: Any) -> Any:
        """Redefine a senha: ``POST /auth/password/reset``.

        :param body: ``reset_token``, ``password``, ``password_confirmation``
        """
        return self.http.post("/auth/password/reset", body, **options)

    def password_resend(self, body: Json, **options: Any) -> Any:
        """Reenvia o código de recuperação: ``POST /auth/password/resend``."""
        return self.http.post("/auth/password/resend", body, **options)

    def change_password(self, body: Json, **options: Any) -> Any:
        """Troca a senha logado: ``POST /password/change``.

        :param body: ``current_password``, ``password``, ``password_confirmation``
        """
        return self.http.post("/password/change", body, **options)

    def profile(self, **options: Any) -> Any:
        """Perfil completo (com estatísticas): ``POST /profile``."""
        return self.http.post("/profile", None, **options)

    def me(self, **options: Any) -> Any:
        """Perfil atual: ``GET /profile/me``."""
        return self.http.get("/profile/me", **options)

    def update_me(self, body: Json, **options: Any) -> Any:
        """Atualiza o perfil: ``PUT /profile/me``."""
        return self.http.put("/profile/me", body, **options)

    def verify(self, **options: Any) -> Any:
        """Valida o token atual: ``GET /auth/verify``."""
        return self.http.get("/auth/verify", **options)

    def refresh(self, **options: Any) -> Any:
        """Renova o JWT: ``POST /refresh``."""
        response = self.http.post("/refresh", None, **options)

        token: Optional[Any] = None
        if isinstance(response, Mapping):
            authorization = response.get("authorization")
            if isinstance(authorization, Mapping):
                token = authorization.get("token")
            if not token:
                token = response.get("token")

        if isinstance(token, str) and token:
            self.http.set_bearer_token(token)

        return response

    def token_rotate(self, **options: Any) -> Any:
        """Rotaciona o token: ``POST /auth/token/rotate``."""
        return self.http.post("/auth/token/rotate", None, **options)

    def token_revoke(self, **options: Any) -> Any:
        """Revoga o token atual: ``POST /auth/token/revoke``."""
        return self.http.post("/auth/token/revoke", None, **options)

    def logout(self, **options: Any) -> Any:
        """Encerra a sessão: ``POST /auth/logout``."""
        response = self.http.post("/auth/logout", None, **options)
        self.http.set_bearer_token(None)

        return response

    def _store_token(self, response: Any) -> None:
        """Guarda o Bearer Token quando a resposta trouxer ``authorization.token``."""
        if not isinstance(response, Mapping):
            return

        authorization = response.get("authorization")
        if not isinstance(authorization, Mapping):
            return

        token = authorization.get("token")
        if isinstance(token, str) and token:
            self.http.set_bearer_token(token)
