from pathlib import Path
from typing import Optional
from sqlalchemy import Connection, Engine, URL, create_engine


class SQLEngine:
    """
    A class for creating and connecting to SQL engines.

    :param driver: Optional[str] - The driver for the SQL engine.
    :param host: Optional[str] - The host address for the SQL engine.
    :param database: Optional[str] - The name of the database to connect to.
    :param query: Optional[dict[str, str]] - The additional query parameters to include in the connection URL.

    :ivar driver: Optional[str] - The driver for the SQL engine.
    :ivar host: Optional[str] - The host address for the SQL engine.
    :ivar database: Optional[str] - The name of the database to connect to.
    :ivar query: Optional[dict[str, str]] - The additional query parameters to include in the connection URL.
    :ivar url: URL - The connection URL for the SQL engine.
    :ivar engine: Engine - The SQLAlchemy engine object.

    """
    def __init__(
            self,
            driver: Optional[str],
            host: Optional[str],
            database: Optional[str], query: Optional[dict[str, str]],
            **kwargs
    ) -> None:
        self.driver = driver
        self.host = host
        self.database = database
        self.query = query

        self.url = URL.create(
            drivername=self.driver,
            host=self.host,
            database=self.database,
            query=self.query,
            **kwargs
        )

        self.engine = create_engine(url=self.url)

    def connect(self) -> Connection:
        return self.engine.connect()


class MSSQLEngine(SQLEngine):
    """
    A class representing an MSSQL database engine.

    The MSSQLEngine class inherits from the SQLEngine class
    and provides the necessary functionality to connect
    to an MSSQL database and execute SQL queries.

    Attributes:
        driver (str): The driver used for connecting to the database.
        query (dict[str, str]): The additional query parameters to be used for connecting to the database.

    Methods:
        __init__(self, host: str, database: str) -> None: Initializes a new instance of the MSSQLEngine class.

    """
    driver: str = "mssql+pyodbc"
    query: dict[str, str] = {"driver": "SQL Server Native Client 11.0"}

    def __init__(self, host: str, database: str) -> None:
        super().__init__(
            driver=self.driver,
            host=host,
            database=database,
            query=self.query
        )


class AccessEngine(SQLEngine):
    """
    AccessEngine class
    ------------------

    This class represents an AccessEngine that is used for accessing a Microsoft Access database using the pyodbc driver.

    Attributes:
    -----------
    - driver (str): The driver used for connecting to the Access database.
    - query (dict[str, str]): The query parameters used for the connection.
        - driver: The driver specification for the Access database.
        - ExtendedAnsiSql: The setting for enabling extended ANSI SQL.

    Methods:
    --------
    - __init__(self, db_path: str | Path) -> None:
        Initializes the AccessEngine instance.
        Parameters:
            - db_path (str | Path): The path to the Access database.
    """
    driver: str = "access+pyodbc"
    query: dict[str, str] = {
        "driver": "Microsoft Access Driver (*.mdb, *.accdb)",
        "ExtendedAnsiSql": "1"
    }

    def __init__(self, db_path: str | Path) -> None:
        self.query["DBQ"] = str(Path(db_path).absolute())
        super().__init__(
            driver=self.driver,
            host=None,
            database=None,
            query=self.query
        )


def build_engine(
        driver: str = None,
        host: str = None,
        database: str = None,
        query: dict[str, str] = None,
        local_db_filepath: str | Path = None
) -> Engine:
    """
    Build and return a database engine based on the provided configurations.

    :param driver: The database driver to use.
    :type driver: str, optional
    :param host: The host of the database.
    :type host: str, optional
    :param database: The name of the database.
    :type database: str, optional
    :param query: Additional query parameters for the database engine.
    :type query: dict[str, str], optional
    :param local_db_filepath: The filepath to a local database file.
    :type local_db_filepath: str or Path, optional
    :return: The instantiated database engine.
    :rtype: Engine
    :raises AssertionError: If neither driver nor local_db_filepath is provided.
    """
    assert driver is not None or local_db_filepath is not None, "Specify a driver or local database file path."

    if driver == "mssql":
        return MSSQLEngine(
            host=host,
            database=database
        ).engine

    elif driver == "access":
        assert local_db_filepath is not None, "Using Access you must specify a local database file path."
        return AccessEngine(db_path=local_db_filepath).engine

    else:
        try:
            return SQLEngine(
                driver=driver,
                host=host,
                database=database,
                query=query
            ).engine
        except Exception as e:
            raise e
