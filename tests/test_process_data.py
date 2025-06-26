import pytest

from app.services.external_api import fetch_cat_fact
from app.models.schemas import CatFactResponse
from httpx import AsyncClient
from fastapi import status
from app.main import app



@pytest.mark.asyncio
async def test_fetch_cat_fact_returns_valid_response():
    result = await fetch_cat_fact()
    assert isinstance(result, CatFactResponse)
    assert isinstance(result.fact, str)
    assert isinstance(result.length, int)
    assert result.length == len(result.fact)

"""
Тесты для проекта FastAPI.
Для успешного прохождения тестов, FastAPI-приложение и Redis должны быть запущены через Docker:
    docker-compose up --build
Эти тесты отправляют реальные HTTP-запросы на http://localhost:8080
"""


@pytest.mark.asyncio
async def test_process_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/process_data/", json={"name": "Behan"})
        assert response.status_code == status.HTTP_200_OK
        json_data = response.json()
        assert "processed_at" in json_data["processed_data"]
        assert json_data["processed_data"]["name"] == "Behan"
        assert "cat_fact" in json_data

@pytest.mark.asyncio
async def test_get_history():
    async with AsyncClient(base_url="http://localhost:8080") as ac:
        response = await ac.post("/process_data/", json={"name": "Behan"})
        data = response.json()
        assert isinstance(data, dict)
        assert "processed_data" in data
        assert "cat_fact" in data
        assert "name" in data["processed_data"]

@pytest.mark.asyncio
async def test_history_endpoint():
    async with AsyncClient(base_url="http://localhost:8080") as ac:
        await ac.post("/process_data/", json={"name": "Behan"})

        response = await ac.get("/process_data/history/?n=1")
        assert response.status_code == status.HTTP_200_OK

        history = response.json()
        assert isinstance(history, list)
        assert len(history) >= 1

        entry = history[0]
        assert "method" in entry
        assert "url" in entry
        assert "timestamp" in entry
        assert "input" in entry
        assert "response" in entry
        assert "status_code" in entry

