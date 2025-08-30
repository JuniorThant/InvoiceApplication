from __future__ import annotations

import binascii
import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Final

from advanced_alchemy.utils.text import slugify
from litestar.data_extractors import RequestExtractorField, ResponseExtractorField
from litestar.serialization import decode_json, encode_json
from litestar.utils.module_loader import module_to_os_path
from redis.asyncio import Redis
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from ._utils import get_env

DEFAULT_MODULE_NAME = "app"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)


@dataclass
class DatabaseSettings:
    ECHO: bool = field(default_factory=get_env("DATABASE_ECHO", False))
    ECHO_POOL: bool = field(default_factory=get_env("DATABASE_ECHO_POOL", False))
    POOL_DISABLED: bool = field(default_factory=get_env("DATABASE_POOL_DISABLED", False))
    POOL_MAX_OVERFLOW: int = field(default_factory=get_env("DATABASE_MAX_POOL_OVERFLOW", 10))
    POOL_SIZE: int = field(default_factory=get_env("DATABASE_POOL_SIZE", 5))
    POOL_TIMEOUT: int = field(default_factory=get_env("DATABASE_POOL_TIMEOUT", 30))
    POOL_RECYCLE: int = field(default_factory=get_env("DATABASE_POOL_RECYCLE", 300))
    POOL_PRE_PING: bool = field(default_factory=get_env("DATABASE_PRE_POOL_PING", False))
    URL: str = field(default_factory=get_env("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3"))
    MIGRATION_CONFIG: str = field(
        default_factory=get_env("DATABASE_MIGRATION_CONFIG", f"{BASE_DIR}/db/migrations/alembic.ini")
    )
    MIGRATION_PATH: str = field(default_factory=get_env("DATABASE_MIGRATION_PATH", f"{BASE_DIR}/db/migrations"))
    MIGRATION_DDL_VERSION_TABLE: str = field(
        default_factory=get_env("DATABASE_MIGRATION_DDL_VERSION_TABLE", "ddl_version")
    )
    FIXTURE_PATH: str = field(default_factory=get_env("DATABASE_FIXTURE_PATH", f"{BASE_DIR}/db/fixtures"))
    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance

        common_args = dict(
            url=self.URL,
            future=True,
            json_serializer=encode_json,
            json_deserializer=decode_json,
            echo=self.ECHO,
            echo_pool=self.ECHO_POOL,
            pool_recycle=self.POOL_RECYCLE,
            pool_pre_ping=self.POOL_PRE_PING,
        )

        if self.URL.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                **common_args,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_use_lifo=True,
                poolclass=NullPool if self.POOL_DISABLED else None,
            )

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:
                def encoder(bin_value: bytes) -> bytes:
                    return b"\x01" + encode_json(bin_value)

                def decoder(bin_value: bytes) -> Any:
                    return decode_json(bin_value[1:])

                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "jsonb", encoder=encoder, decoder=decoder, schema="pg_catalog", format="binary"
                    )
                )
                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "json", encoder=encoder, decoder=decoder, schema="pg_catalog", format="binary"
                    )
                )
        elif self.URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(**common_args)

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "begin")
            def _sqla_on_begin(dbapi_connection: Any) -> Any:
                dbapi_connection.exec_driver_sql("BEGIN")
        else:
            engine = create_async_engine(
                **common_args,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_use_lifo=True,
                poolclass=NullPool if self.POOL_DISABLED else None,
            )

        self._engine_instance = engine
        return engine


@dataclass
class ViteSettings:
    DEV_MODE: bool = field(default_factory=get_env("VITE_DEV_MODE", False))
    USE_SERVER_LIFESPAN: bool = field(default_factory=get_env("VITE_USE_SERVER_LIFESPAN", True))
    HOST: str = field(default_factory=get_env("VITE_HOST", "0.0.0.0"))  # noqa: S104
    PORT: int = field(default_factory=get_env("VITE_PORT", 5173))
    HOT_RELOAD: bool = field(default_factory=get_env("VITE_HOT_RELOAD", True))
    ENABLE_REACT_HELPERS: bool = field(default_factory=get_env("VITE_ENABLE_REACT_HELPERS", True))
    BUNDLE_DIR: Path = field(default_factory=get_env("VITE_BUNDLE_DIR", Path(f"{BASE_DIR}/domain/web/public")))
    RESOURCE_DIR: Path = field(default_factory=get_env("VITE_RESOURCE_DIR", Path("resources")))
    TEMPLATE_DIR: Path = field(default_factory=get_env("VITE_TEMPLATE_DIR", Path(f"{BASE_DIR}/domain/web/templates")))
    ASSET_URL: str = field(default_factory=get_env("ASSET_URL", "/static/"))

    @property
    def set_static_files(self) -> bool:
        return self.ASSET_URL.startswith("/")


@dataclass
class ServerSettings:
    HOST: str = field(default_factory=get_env("LITESTAR_HOST", "0.0.0.0"))  # noqa: S104
    PORT: int = field(default_factory=get_env("LITESTAR_PORT", 8000))
    KEEPALIVE: int = field(default_factory=get_env("LITESTAR_KEEPALIVE", 65))
    RELOAD: bool = field(default_factory=get_env("LITESTAR_RELOAD", False))
    RELOAD_DIRS: list[str] = field(default_factory=get_env("LITESTAR_RELOAD_DIRS", [f"{BASE_DIR}"], list[str]))


@dataclass
class SaqSettings:
    PROCESSES: int = field(default_factory=get_env("SAQ_PROCESSES", 1))
    CONCURRENCY: int = field(default_factory=get_env("SAQ_CONCURRENCY", 10))
    WEB_ENABLED: bool = field(default_factory=get_env("SAQ_WEB_ENABLED", True))
    USE_SERVER_LIFESPAN: bool = field(default_factory=get_env("SAQ_USE_SERVER_LIFESPAN", True))


@dataclass
class LogSettings:
    EXCLUDE_PATHS: str = r"\A(?!x)x"
    HTTP_EVENT: str = "HTTP"
    INCLUDE_COMPRESSED_BODY: bool = False
    LEVEL: int = field(default_factory=get_env("LOG_LEVEL", 30))
    OBFUSCATE_COOKIES: set[str] = field(default_factory=lambda: {"session", "XSRF-TOKEN"})
    OBFUSCATE_HEADERS: set[str] = field(default_factory=lambda: {"Authorization", "X-API-KEY", "X-XSRF-TOKEN"})
    JOB_FIELDS: list[str] = field(
        default_factory=lambda: [
            "function",
            "kwargs",
            "key",
            "scheduled",
            "attempts",
            "completed",
            "queued",
            "started",
            "result",
            "error",
        ]
    )
    REQUEST_FIELDS: list[RequestExtractorField] = field(
        default_factory=get_env(
            "LOG_REQUEST_FIELDS", ["path", "method", "query", "path_params"], list[RequestExtractorField]
        )
    )
    RESPONSE_FIELDS: list[ResponseExtractorField] = field(
        default_factory=get_env("LOG_RESPONSE_FIELDS", ["status_code"], list[ResponseExtractorField])
    )
    WORKER_EVENT: str = "Worker"
    SAQ_LEVEL: int = field(default_factory=get_env("SAQ_LOG_LEVEL", 50))
    SQLALCHEMY_LEVEL: int = field(default_factory=get_env("SQLALCHEMY_LOG_LEVEL", 30))
    ASGI_ACCESS_LEVEL: int = field(default_factory=get_env("ASGI_ACCESS_LOG_LEVEL", 30))
    ASGI_ERROR_LEVEL: int = field(default_factory=get_env("ASGI_ERROR_LOG_LEVEL", 30))


@dataclass
class RedisSettings:
    URL: str = field(default_factory=get_env("REDIS_URL", "redis://localhost:6379/0"))
    SOCKET_CONNECT_TIMEOUT: int = field(default_factory=get_env("REDIS_CONNECT_TIMEOUT", 5))
    HEALTH_CHECK_INTERVAL: int = field(default_factory=get_env("REDIS_HEALTH_CHECK_INTERVAL", 5))
    SOCKET_KEEPALIVE: bool = field(default_factory=get_env("REDIS_SOCKET_KEEPALIVE", True))

    @property
    def client(self) -> Redis:
        return self.get_client()

    def get_client(self) -> Redis:
        return Redis.from_url(
            url=self.URL,
            encoding="utf-8",
            decode_responses=False,
            socket_connect_timeout=self.SOCKET_CONNECT_TIMEOUT,
            socket_keepalive=self.SOCKET_KEEPALIVE,
            health_check_interval=self.HEALTH_CHECK_INTERVAL,
        )


@dataclass
class AppSettings:
    APP_LOC: str = "app.asgi:create_app"
    URL: str = field(default_factory=get_env("APP_URL", "http://localhost:8015"))
    DEBUG: bool = field(default_factory=get_env("LITESTAR_DEBUG", False))
    SECRET_KEY: str = field(default_factory=get_env("SECRET_KEY", binascii.hexlify(os.urandom(32)).decode("utf-8")))
    NAME: str = field(default_factory=lambda: "app")
    ALLOWED_CORS_ORIGINS: list[str] | str = field(default_factory=get_env("ALLOWED_CORS_ORIGINS", ["*"]))
    CSRF_COOKIE_NAME: str = field(default_factory=get_env("CSRF_COOKIE_NAME", "XSRF-TOKEN"))
    CSRF_COOKIE_SECURE: bool = field(default_factory=get_env("CSRF_COOKIE_SECURE", False))
    JWT_ENCRYPTION_ALGORITHM: str = field(default_factory=lambda: "HS256")
    GITHUB_OAUTH2_CLIENT_ID: str = field(default_factory=get_env("GITHUB_OAUTH2_CLIENT_ID", ""))
    GITHUB_OAUTH2_CLIENT_SECRET: str = field(default_factory=get_env("GITHUB_OAUTH2_CLIENT_SECRET", ""))

    SMTP_SERVER: str = field(default_factory=get_env("SMTP_SERVER", "smtp.mailtrap.io"))
    SMTP_PORT: int = field(default_factory=get_env("SMTP_PORT", 587))
    SMTP_USER: str = field(default_factory=get_env("MAILTRAP_USER", "254e5790826d47"))
    SMTP_PASS: str = field(default_factory=get_env("MAILTRAP_PASS", "f74b2140e411aa"))
    SENDER: str = field(default_factory=get_env("SENDER", "no-reply@example.com"))

    CLOUD_NAME: str = field(default_factory=get_env("CLOUD_NAME", "dqtudbhm1"))
    CLOUD_API_KEY: str = field(default_factory=get_env("CLOUD_API_KEY", "281978128992832"))
    CLOUD_API_SECRET: str = field(default_factory=get_env("CLOUD_API_SECRET", "H1AS_rUqO-Cmak9YHQ3Pl1zyUJ8"))
    CLOUDINARY_URL: str = field(
        default_factory=get_env("CLOUDINARY_URL", "cloudinary://281978128992832:H1AS_rUqO-Cmak9YHQ3Pl1zyUJ8@dqtudbhm1")
    )

    ADMIN_SECRET:str=field(default_factory=get_env("ADMIN_SECRET","c1353344"))

    @property
    def slug(self) -> str:
        return slugify(self.NAME)

    def __post_init__(self) -> None:
        if isinstance(self.ALLOWED_CORS_ORIGINS, str):
            try:
                self.ALLOWED_CORS_ORIGINS = json.loads(self.ALLOWED_CORS_ORIGINS)
            except ValueError:
                self.ALLOWED_CORS_ORIGINS = [host.strip() for host in self.ALLOWED_CORS_ORIGINS.split(",")]


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    vite: ViteSettings = field(default_factory=ViteSettings)
    server: ServerSettings = field(default_factory=ServerSettings)
    log: LogSettings = field(default_factory=LogSettings)
    redis: RedisSettings = field(default_factory=RedisSettings)
    saq: SaqSettings = field(default_factory=SaqSettings)

    @classmethod
    def from_env(cls, dotenv_filename: str = ".env") -> Settings:
        from litestar.cli._utils import console

        env_file = Path(f"{os.curdir}/{dotenv_filename}")
        if env_file.is_file():
            from dotenv import load_dotenv

            console.print(f"[yellow]Loading environment configuration from {dotenv_filename}[/]")
            load_dotenv(env_file, override=True)
        return Settings()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.from_env()
