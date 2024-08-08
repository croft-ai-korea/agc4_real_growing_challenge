import sys
from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor, execute_batch, execute_values
from psycopg2 import pool
import pandas as pd

sys.path.append('./')
from aaaa.config import config
from a_util.db.schema import create_measure_table_query, create_simulation_table_query
from a_util.db.schema import simulation_data_insert_query
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

def create_table_if_not_exists(table_name:str, query:str):
    check_table_query = f"""
    SELECT EXISTS (
        SELECT FROM pg_tables
        WHERE schemaname = 'public' AND tablename = '{table_name}'
    );
    """
    
    with pool.getconn() as conn:
        cursor = conn.cursor()
        cursor.execute(check_table_query)
        exists = cursor.fetchone()[0]

        if not exists:
            cursor.execute(query)
            conn.commit()
            print(f"Table {table_name} created.")
        else:
            print(f"Table {table_name} already exists.")
        pool.putconn(conn)    

def db_drop_table_if_exists(table_name: str):
    drop_table_query = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    
    with pool.getconn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(drop_table_query)
            conn.commit()
            print(f"Table '{table_name}' has been dropped.")
        except Exception as e:
            print(f"Error dropping table '{table_name}':", e)
        finally:
            pool.putconn(conn)

def db_simulation_data_insert(df:pd.DataFrame):
    data_tuples = [tuple(x) for x in df.to_numpy()]
    with pool.getconn() as conn:
        cursor = conn.cursor()
        try:
            execute_values(cursor, simulation_data_insert_query, data_tuples)
            conn.commit()  # 데이터 삽입 후 커밋
        except Exception as e:
            print(f"Error inserting simulation data: {e}")
            conn.rollback()  # 오류 발생 시 
        finally:
            pool.putconn(conn)
        
if __name__ == "__main__":
    # create_table_if_not_exists(table_name='measure', query=create_measure_table_query)
    create_table_if_not_exists(table_name='simulation', query=create_simulation_table_query)
    
    # db_drop_table_if_exists('measure')
    
    # r = db_select(""" select * from measure """)
    # print(r)
