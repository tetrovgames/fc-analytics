import unittest

from sqlmodel import create_engine, select, Session


class DbIntegrationTest(unittest.TestCase):

    def test_db_connection(self) -> None:
        database_url = ""
        # connect_args={"sslmode": "disable"}
        self.engine = create_engine(database_url, pool_pre_ping=True)
        with Session(self.engine) as session:
            result = session.exec(select(1)).first()
            self.assertEqual(1, result)
