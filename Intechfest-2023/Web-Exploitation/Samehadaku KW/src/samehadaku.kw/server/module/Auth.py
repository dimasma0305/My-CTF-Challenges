from datetime import timedelta
from typing import Dict, Optional, Sequence, Union
from fastapi import Depends, HTTPException, Request, Response
from fastapi_jwt_auth import AuthJWT
import json
from pydantic import BaseModel

from module.sanitizer import sanitize_path
from . import configparse
import os


class Auth(AuthJWT):
    def __init__(self, req: Request = None, res: Response = None):
        super().__init__(req, res)

    def create_access_token(
        self,
        subject: "User",
        fresh: Optional[bool] = False,
        algorithm: Optional[str] = None,
        headers: Optional[Dict] = None,
        expires_time: Optional[Union[timedelta, int, bool]] = None,
        audience: Optional[Union[str, Sequence[str]]] = None,
        user_claims: Optional[Dict] = {}
    ) -> str:
        return super().create_access_token(
            subject.to_json(),
            fresh,
            algorithm,
            headers,
            expires_time,
            audience,
            user_claims
        )

    def get_jwt_subject(self) -> Union["User", None]:
        subject = super().get_jwt_subject()
        if not subject:
            return None
        return User.from_json(subject)


class User(BaseModel):
    username: str
    isAdmin: Optional[bool]
    configfile: Optional[str]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @classmethod
    def from_json(cls, json_str) -> "User":
        return cls(**json.loads(json_str))

    def config(self):
        return configparse.parse("config/"+sanitize_path(self.configfile))


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ['SECRET_KEY']
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@Auth.load_config
def get_config():
    return Settings()


async def authorize_user(Authorize: Auth = Depends()):
    try:
        Authorize.jwt_required()
        user = Authorize.get_jwt_subject()
    except Exception as e:
        print(e)
        user = User(
            username="guest",
            isAdmin=False,
            configfile="default.conf.yaml"
        )
        access_token = Authorize.create_access_token(user)
        Authorize.set_access_cookies(access_token)
    return user


async def must_admin(Authorize: Auth = Depends()):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    if not user or not user.isAdmin:
        raise HTTPException(403, "Forbidden")
    return user
