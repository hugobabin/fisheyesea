"""Service for handling MariaDB operations."""

import mariadb
from mariadb.connections import Connection
from mariadb.cursors import Cursor


class ServiceMaria:
    """ServiceMaria."""

    con: Connection = None
    cur: Cursor = None

    @classmethod
    def get_cursor(cls) -> Cursor:
        """Get MariaDB cursor."""
        if cls.cur is not None:
            return cls.cur
        cls.con: Connection = mariadb.connect(
            user="root",
            password="example",
            host="localhost",
            port=3306,
            database="fisheyesea",
        )
        cls.cur = cls.con.cursor()
        return cls.cur

    @classmethod
    def close_connection(cls):
        """Close MariaDB connector."""
        cls.con.close()
        cls.cur.close()
        cls.cur = None
        cls.con = None
