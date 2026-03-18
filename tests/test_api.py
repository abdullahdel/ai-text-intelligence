from fastapi.testclient import TestClient
from fastapi import HTTPException
from app import main

def test_post_analyze_success(monkeypatch):
    called = {}

    def fake_create_analysis(text):
        called["text"] = text
        return {"analysis": "Test analysis" }

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "create_analysis", fake_create_analysis)

    with TestClient(main.app) as client:
        response = client.post("/analyze", json={"text": "Hello world"})

    assert response.status_code == 200
    assert response.json() == {"analysis": "Test analysis"}
    assert called["text"] == "Hello world"

def test_post_analyze_error(monkeypatch):
    def fake_create_analysis(text):
        raise HTTPException(status_code=400, detail="Empty text not allowed")

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "create_analysis", fake_create_analysis)

    with TestClient(main.app) as client:
        response = client.post("/analyze", json={"text": ""})

    assert response.status_code == 400
    assert response.json() == {"detail": "Empty text not allowed"}

def test_post_upload_analyze_success(monkeypatch):
    called = {}

    def fake_create_analysis(text, source_type="manual", source_name=None):
        called["text"] = text
        called["source_type"] = source_type
        called["source_name"] = source_name
        return {"analysis": "Uploaded file analysis"}

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "create_analysis", fake_create_analysis)

    with TestClient(main.app) as client:
        response = client.post(
            "/upload-analyze",
            files={"file": ("notes.txt", b"Hello from file", "text/plain")}
        )

    assert response.status_code == 200
    assert response.json() == {"analysis": "Uploaded file analysis"}
    assert called["text"] == "Hello from file"
    assert called["source_type"] == "file"
    assert called["source_name"] == "notes.txt"

def test_post_upload_analyze_error(monkeypatch):
    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)

    with TestClient(main.app) as client:
        response = client.post(
            "/upload-analyze",
            files={"file": ("notes.pdf", b"Hello from file", "text/plain")}
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Nur .txt-Dateien sind erlaubt."}

def test_get_analyses_success(monkeypatch):
    fake_analyses = [
        {
            "id": 1,
            "input_text": "Manual text",
            "analysis": "Manual analysis",
            "source_type": "manual",
            "source_name": None,
            "created_at": "2026-03-16T12:00:00"
        },
        {
            "id": 2,
            "input_text": "File text",
            "analysis": "File analysis",
            "source_type": "file",
            "source_name": "notes.txt",
            "created_at": "2026-03-16T12:05:00"
        }
    ]
    def fake_list_analyses(limit, offset):
        return fake_analyses

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "list_analyses", fake_list_analyses)

    with TestClient(main.app) as client:
        response = client.get("/analyses?limit=5&offset=0")

    assert response.status_code == 200
    assert response.json() == fake_analyses

def test_get_analysis_by_id_success(monkeypatch):
    fake_analysis = {
        "id": 7,
        "input_text": "Some text",
        "analysis": "Detailed analysis",
        "source_type": "file",
        "source_name": "notes.txt",
        "created_at": "2026-03-16T12:10:00"
    }
    def fake_get_analysis_service(analysis_id):
        return fake_analysis

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "get_analysis_service", fake_get_analysis_service)

    with TestClient(main.app) as client:
        response = client.get("/analyses/7")

    assert response.status_code == 200
    assert response.json() == fake_analysis

def test_get_analysis_by_id_not_found(monkeypatch):
    def fake_get_analysis_service(analysis_id):
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "get_analysis_service", fake_get_analysis_service)

    with TestClient(main.app) as client:
        response = client.get("/analyses/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Analyse nicht gefunden"}

def test_delete_analysis_success(monkeypatch):
    def fake_delete_analysis_by_id(analysis_id):
        return {"message": "Analysis deleted"}

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "delete_analysis_by_id", fake_delete_analysis_by_id)

    with TestClient(main.app) as client:
        response = client.delete("/analyses/7")

    assert response.status_code == 200
    assert response.json() == {"message": "Analysis deleted"}

def test_delete_analysis_not_found(monkeypatch):
    def fake_delete_analysis_by_id(analysis_id):
        raise HTTPException(status_code=404, detail="Analyse nicht gefunden")

    monkeypatch.setattr(main, "init_pool", lambda: None)
    monkeypatch.setattr(main, "init_db", lambda: None)
    monkeypatch.setattr(main, "delete_analysis_by_id", fake_delete_analysis_by_id)

    with TestClient(main.app) as client:
        response = client.delete("/analyses/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Analyse nicht gefunden"}










