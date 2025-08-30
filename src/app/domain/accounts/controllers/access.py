"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from advanced_alchemy.utils.text import slugify
from litestar import Controller, Request, Response, get, patch, post
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body, Parameter

from app.config.base import get_settings
from app.domain.accounts import urls
from app.domain.accounts.deps import provide_users_service
from app.domain.accounts.guards import auth, requires_active_user, requires_superuser
from app.domain.accounts.schemas import AccountLogin, AccountRegister, User
from app.domain.accounts.services import RoleService
from app.lib.deps import create_service_provider

if TYPE_CHECKING:
    from litestar.security.jwt import OAuth2Login

    from app.db import models as m
    from app.domain.accounts.services import UserService

settings = get_settings()
ADMIN_SECRET = settings.app.ADMIN_SECRET


class AccessController(Controller):
    """User login and registration."""

    tags = ["Access"]
    dependencies = {
        "users_service": Provide(provide_users_service),
        "roles_service": Provide(create_service_provider(RoleService)),
    }

    @post(operation_id="AccountLogin", path=urls.ACCOUNT_LOGIN, exclude_from_auth=True)
    async def login(
        self,
        users_service: UserService,
        data: Annotated[AccountLogin, Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED)],
    ) -> Response[OAuth2Login]:
        """Authenticate a user."""
        user = await users_service.authenticate(data.username, data.password)
        return auth.login(user.email)

    @post(operation_id="AccountLogout", path=urls.ACCOUNT_LOGOUT, exclude_from_auth=True)
    async def logout(self, request: Request) -> Response:
        """Account Logout"""
        request.cookies.pop(auth.key, None)
        request.clear_session()

        response = Response(
            {"message": "OK"},
            status_code=200,
        )
        response.delete_cookie(auth.key)

        return response

    @post(operation_id="AccountRegister", path=urls.ACCOUNT_REGISTER)
    async def signup(
        self,
        request: Request,
        users_service: UserService,
        roles_service: RoleService,
        data: AccountRegister,
    ) -> User:
        """User Signup."""
        try:
            user_data = data.to_dict()
            if data.secret:
                if data.secret == ADMIN_SECRET:
                    user_data["is_superuser"] = True
                else:
                    raise HTTPException(status_code=400, detail="The admin secret is not correct")

            role_obj = await roles_service.get_one_or_none(slug=slugify(users_service.default_role))
            if role_obj is not None:
                user_data.update({"role_id": role_obj.id})
            user = await users_service.create(user_data)
            request.app.emit(event_id="user_created", user_id=user.id)
            return users_service.to_schema(user, schema_type=User)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @patch(operation_id="ChangeRole", path=urls.CHANGE_ROLE, guards=[requires_superuser])
    async def change_role(
        self, user_id: Annotated[UUID, Parameter(title="User ID")], users_service: UserService, current_user: m.User
    ) -> dict:
        try:
            user = await users_service.get_one_or_none(id=user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            new_value = not user.is_superuser

            updated_user = await users_service.update(
                item_id=user_id,
                data={"is_superuser": new_value}
            )
            return {
                "message": "User role updated successfully",
                "updated_user": users_service.to_schema(updated_user, schema_type=User)
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    @get(operation_id="AccountProfile", path=urls.ACCOUNT_PROFILE, guards=[requires_active_user])
    async def profile(self, current_user: m.User, users_service: UserService) -> User:
        """User Profile."""
        return users_service.to_schema(current_user, schema_type=User)
