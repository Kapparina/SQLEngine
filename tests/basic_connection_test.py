from src.sqlengine.sqlengine import build_engine, Engine


driver: str = input("Enter the driver: ")
host: str = input("Enter the host: ")
database: str = input("Enter the database: ")

if len(host) == 0 or driver == "access":
    db_path: str = input("Enter the path to the database: ")
    engine: Engine = build_engine(
        driver=driver,
        local_db_filepath=db_path
    )
else:
    engine: Engine = build_engine(
        driver=driver,
        host=host,
        database=database
    )

print(engine.url)
print(engine.connect())
