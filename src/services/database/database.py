# External imports:
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from threading import Lock
from typing import Optional
from logging import getLogger
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Internal imports:
from .models import BaseModel

# Code:
class DatabaseService:
    """
    This class provides an interface for managing database connections and sessions. It allows for the creation, retrieval, and
    deletion of asynchronous engines for connecting to the database. The service can be extended to include additional
    functionality as needed.
    """
    # Attributes:
    _instance_lock = Lock()
    _instance: Optional["DatabaseService"] = None

    # Internal methods:
    def __init__(self) -> None:
        """
        Initializes the DatabaseService only once. Subsequent constructions return the same instance without
        reinitializing internal state.
        """
        if getattr(self, "_initialized", False):
            return

        self._engines: dict[str, dict] = {}
        self._initialized = True
        self._logger = getLogger(__package__)

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of DatabaseService is created (Singleton pattern). If an instance already exists, it returns that instance instead of creating a new one.
        """
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

    # Private methods:

    # Public methods:
    def create_engine(self, name: str, database_url: str, **engine_kwargs) -> None:
        """
        Creates an asynchronous engine for connecting to the database.

        :param name: The name of the engine to create. This can be used to identify the engine later when retrieving it.
        :type name: str
        :param database_url: The URL of the database to connect to.
        :type database_url: str
        :param engine_kwargs: Additional keyword arguments to pass to the create_async_engine function when creating the engine.
        :raises ValueError: If an engine with the given name already exists.
        """
        if name in self._engines:
            raise ValueError(f"An engine with the name '{name}' already exists.")

        default_engine_kwargs = {
            "echo": False,
            "pool_pre_ping": True,
        }
        engine_kwargs = {**default_engine_kwargs, **engine_kwargs}

        engine = create_async_engine(database_url, **engine_kwargs)
        session_maker = async_sessionmaker(engine, expire_on_commit=False)
        self._engines[name] = {"engine": engine, "session_maker": session_maker}

    def get_engine(self, name: str) -> AsyncEngine:
        """
        Retrieves an asynchronous engine by its name.

        :param name: The name of the engine to retrieve.
        :type name: str
        :return: The asynchronous engine associated with the given name.
        :rtype: AsyncEngine
        :raises ValueError: If no engine is found with the given name.
        """
        if name not in self._engines:
            raise ValueError(f"No engine found with the name '{name}'.")

        return self._engines[name]["engine"]

    @asynccontextmanager
    async def get_session(self, name: str) -> AsyncIterator[AsyncSession]:
        """
        Retrieves an asynchronous session by the engine's name.

        :param name: The name of the engine to retrieve the session from.
        :type name: str
        :return: The asynchronous session associated with the given engine name.
        :rtype: AsyncIterator[AsyncSession]
        :raises ValueError: If no engine is found with the given name.
        """
        if name not in self._engines:
            raise ValueError(f"No engine found with the name '{name}'.")

        async with self._engines[name]["session_maker"]() as session:
            yield session

    async def setup_engine(self, name: str) -> None:
        """
        Sets up an engine by creating all tables defined in the BaseModel metadata.

        :param name: The name of the engine to set up.
        :type name: str
        :raises ValueError: If no engine is found with the given name.
        """
        if name not in self._engines:
            raise ValueError(f"No engine found with the name '{name}'.")

        async with self._engines[name]["engine"].begin() as connection:
            await connection.run_sync(BaseModel.metadata.create_all)

    def check_engine_name(self, name: str) -> bool:
        """
        Checks if an engine with the given name exists.

        :param name: The name of the engine to check.
        :type name: str
        :return: True if an engine with the given name exists, False otherwise.
        :rtype: bool
        """
        return name in self._engines

    async def check_engine_health(self, name: str) -> bool:
        """
        Checks the health of an engine by attempting to connect to the database.

        :param name: The name of the engine to check.
        :type name: str
        :return: True if the engine is healthy, False otherwise.
        :rtype: bool
        :raises ValueError: If no engine is found with the given name.
        """
        if name not in self._engines:
            raise ValueError(f"No engine found with the name '{name}'.")

        try:
            async with self._engines[name]["engine"].connect() as connection:
                await connection.execute(text("SELECT 1"))
            return True

        except SQLAlchemyError as error:
            self._logger.error(f"Database health check failed for engine '{name}': {error}")
            return False

    async def delete_engine(self, name: str) -> None:
        """
        Deletes an asynchronous engine by its name.

        :param name: The name of the engine to delete.
        :type name: str
        :raises ValueError: If no engine is found with the given name.
        """
        if name not in self._engines:
            raise ValueError(f"No engine found with the name '{name}'.")

        await self._engines[name]["engine"].dispose()

        del self._engines[name]
