import os
from sqlalchemy import create_engine
from ..repository.models import SqlAlchemyBase
from sqlalchemy.orm import sessionmaker

class DatabaseUnit:
    def __init__(self):
        __conn_str = (f'postgresql+psycopg2://postgres:'
                    f'{os.environ.get("DBPASSWORD")}@{os.environ.get("SERVER")}:'
                    f'{os.environ.get("PORT")}/{os.environ.get("DBNAME")}')

        self.__engine = create_engine(
            __conn_str,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=2,
            use_insertmanyvalues=True
        )

        self.session_maker = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    def initialize_tables(self):
        SqlAlchemyBase.metadata.create_all(self.__engine)

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
           self.rollback()
           self.session.close()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
