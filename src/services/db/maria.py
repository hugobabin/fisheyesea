"""Service for handling MariaDB operations."""

import mariadb
from mariadb.connections import Connection
from mariadb.cursors import Cursor


class ServiceMaria:
    """ServiceMaria."""

    con: Connection = None
    cur: Cursor = None

    @staticmethod
    def create_database() -> None:
        con = mariadb.connect(
            user="root",
            password="example",
            host="127.0.0.1",
            port=3306,
        )
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS fisheyesea")
        cur.close()
        con.close()

    @classmethod
    def get_cursor(cls) -> Cursor:
        """Get MariaDB cursor."""
        if cls.cur is not None:
            return cls.cur
        cls.con: Connection = mariadb.connect(
            user="root",
            password="example",
            host="127.0.0.1",
            port=3306,
            database="fisheyesea",
        )
        cls.cur = cls.con.cursor()
        return cls.cur

    @classmethod
    def exec(cls, query):
        cls.cur.execute(query)
        cls.con.commit()

    @classmethod
    def close_connection(cls):
        """Close MariaDB connector."""
        if cls.con:
            cls.con.close()
        if cls.cur:
            cls.cur.close()
        cls.cur = None
        cls.con = None
