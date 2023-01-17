import pymysql

from django.db.backends.mysql.base import DatabaseWrapper as _DatabaseWrapper
from dbutils.pooled_db import PooledDB

_pool = None


class DatabaseWrapper(_DatabaseWrapper):
    def _set_autocommit(self, autocommit):
        pass

    def get_new_connection(self, conn_params):
        global _pool
        if not _pool:
            conn_params['creator'] = pymysql
            print(conn_params)
            _pool = PooledDB(**conn_params)
            print('create connections')
        print('get connection')
        return _pool.connection()
