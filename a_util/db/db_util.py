import sys
from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor, execute_batch
from psycopg2 import pool
import pandas as pd

sys.path.append('./')
from aaaa.config import config

timescale_config = config['timescale']


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _create_pool():
    try:
        _pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                   user=timescale_config['username'],
                                                   password=timescale_config['password'],
                                                   host=timescale_config['host'],
                                                   port=timescale_config['port'],
                                                   database=timescale_config['db']
                                                   )
    except:
        eprint('timescaledb connection error')
        raise psycopg2.Error("timescaledb connection error")
    else:
        return _pool


pool = _create_pool()


# ==============================================================

def db_select_one(sql):
    with pool.getconn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()[0]


def db_select(sql):
    with pool.getconn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)
        return cursor.fetchall()

def db_select_by_param(sql, param: dict):
    with pool.getconn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, param)
        return cursor.fetchall()

def db_select_pandas_sql(sql):
    with pool.getconn() as conn:
        result = pd.read_sql(sql, conn)
        result.set_index('time', inplace=True)
        result = result.sort_index(ascending=True)
        result = result.interpolate()
        print(result)
        return result

def db_select_pandas_sql_dict(sql, param):
    """

    """
    with pool.getconn() as conn:
        result = pd.read_sql(sql, conn, params=param)
        result.set_index('time', inplace=True)
        result = result.sort_index(ascending=True)
        result = result.interpolate()
        return result

def db_select_pandas_sql_dict_real(sql, param):
    with pool.getconn() as conn:
        result = pd.read_sql(sql, conn, params=param)
        result.set_index('time', inplace=True)
        result = result.sort_index(ascending=True)
        return result


def db_execute(sql):
    with pool.getconn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)

def db_delete(sql):
    with pool.getconn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)

def db_insert(sql, d):
    with pool.getconn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, d)
        except Exception as e:
            print("error.pgerror",e)
        finally:
            conn.commit()
            pool.putconn(conn)

def db_insert_many(sql, l: List[dict]):

    with pool.getconn() as conn:
        cursor = conn.cursor()

        try:
            cursor.executemany(sql, l)
        except Exception as e:
            print("error.pgerror many ", e)
        finally:
            conn.commit()
            pool.putconn(conn)

if __name__ == "__main__":
    r = db_select(""" select * from measure """)
    print(r)
