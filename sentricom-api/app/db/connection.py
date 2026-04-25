import sqlite3
import os
from contextlib import contextmanager

# DB path (vercel can only write to /tmp)
DB_PATH = os.getenv("DB_PATH", "/tmp/sentricom.db")

# Path protcetion - make sure /tmp exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Get connection
def get_connection():
    """
    Get a new connection to Sentricom SQLite db.
    Returns:
        sqlite3.Connection: includes thread check for write safety / concurrency
        row_factory set to sqlite3.Row for dict-like read access to rows
    """
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

@contextmanager
def db_cursor():
    """
    Context manager helper for SQLite cursor to allow safe simultaneous processes to run in bg. 
    Allows commit/rollback and closes connection after use for transaction-like behavior.
    """

    db = get_connection()
    cursor = db.cursor()

    try:
        yield cursor
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()

# Single row query helper - like select first or default
def fetch_one(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return a single row
    """
    with db_cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

# All rows query helper
def fetch_all(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return all rows
    """
    with db_cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows] 
    
# Execute helper - no return
def execute(query: str, params: tuple = ()):
    """
    Execute a non-SELECT query (INSERT, UPDATE, DELETE) without return
    """

    with db_cursor() as cursor:
        cursor.execute(query, params)

# Execute helper - with return
def execute_and_return(query: str, params: tuple = ()):
    """
    Execute an INSERT query and return the id of last inserted row
    """
    with db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.lastrowid
    

