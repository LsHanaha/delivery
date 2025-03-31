import typing

import sqlalchemy as sa


def build_db_dsn(
    db_dsn: str,
    database_name: str,
    drivername: str = "postgresql",
) -> sa.URL:
    """Parse DSN variable and replace some parts.

    - DSN stored in format postgresql://login:password@/db_placeholder?host=host1&host=host2
    https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#specifying-multiple-fallback-hosts
    - 'db_placeholder' is replaced here with service database name
    - `target_session_attrs` is chosen based on `use_replica` arg
    """
    parsed_db_dsn = sa.make_url(db_dsn)
    db_dsn_query: dict[str, typing.Any] = dict(parsed_db_dsn.query or {})
    return parsed_db_dsn.set(database=database_name, drivername=drivername, query=db_dsn_query)
