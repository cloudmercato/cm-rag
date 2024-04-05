from urllib.parse import urlparse

from sqlalchemy import delete, select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
from psycopg2 import errors as pg_errors

from django.conf import settings
from django.utils.functional import cached_property


class BaseSqlManager:
    id_field = 'key'

    @cached_property
    def pg_params(self):
        url = urlparse(settings.DATABASE_URL)
        return {
            'database': url.path[1:],
            'host': url.hostname,
            'password': url.password,
            'port': url.port,
            'user': url.username,
        }

    @cached_property
    def engine(self):
        engine = create_engine(settings.DATABASE_URL, future=True)
        return engine

    def session(self):
        Session = scoped_session(sessionmaker(bind=self.engine))
        session = Session()
        return session

    @cached_property
    def table_name(self):
        return self.store._kvstore.table_name

    def _execute(self, req, commit=False):
        req = text(req)
        session = self.session()
        try:
            response = session.execute(req)
            if commit:
                session.commit()
        except pg_errors.ProgrammingError as err:
            return []
        except pg_errors.UndefinedTable as err:
            return []
        return response.mappings()

    def get_all(self):
        req = f'SELECT * FROM data_{self.table_name};'
        return self._execute(req)

    def get(self, key):
        req = f"SELECT * FROM data_{self.table_name} WHERE {self.id_field}='{key}';"
        return next(self._execute(req))

    def flush(self):
        req = f'DELETE FROM data_{self.table_name};'
        self._execute(req, commit=True)
