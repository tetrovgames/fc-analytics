import unittest
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session


class ApiTest(unittest.TestCase):

    def setUp(self) -> None:
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},  # sqlite-specific
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            def get_session_override():
                return session

        app.dependency_overrides[get_session] = get_session_override
        self.client = TestClient(app)

    def test_get_root_not_found(self) -> None:
        response = self.client.get("/")
        self.assertEqual(404, response.status_code)

    def test_get_docs_not_found(self) -> None:
        response = self.client.get("/docs")
        self.assertEqual(404, response.status_code)

    def test_get_redoc_not_found(self) -> None:
        response = self.client.get("/redoc")
        self.assertEqual(404, response.status_code)

    def test_get_statistics(self) -> None:
        response = self.client.get("/statistics")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0},
            response.json())

    def test_save_statistics(self) -> None:
        response = self.client.post(
            "/statistics", json={"lady_id": 0, "user_id": str(uuid.uuid4())})
        self.assertEqual(201, response.status_code)
        self.assertEqual({}, response.json())

    def test_save_and_get_statistics(self) -> None:
        self.client.post("/statistics", json={"lady_id": 0, "user_id": str(uuid.uuid4())})
        self.client.post("/statistics", json={"lady_id": 0, "user_id": str(uuid.uuid4())})
        self.client.post("/statistics", json={"lady_id": 1, "user_id": str(uuid.uuid4())})

        response = self.client.get("/statistics")
        self.assertEqual(
            {"0": 0.667, "1": 0.333, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0},
            response.json())
