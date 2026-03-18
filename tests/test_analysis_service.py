import pytest
from fastapi import HTTPException

from app.services import analysis_service


def test_create_analysis_success_manual(monkeypatch):
    saved = {}

    def fake_analyze_text(text):
        return {"analysis": "Test analysis"}

    def fake_save_analysis(input_text, analysis, source_type="manual", source_name=None):
        saved["input_text"] = input_text
        saved["analysis"] = analysis
        saved["source_type"] = source_type
        saved["source_name"] = source_name

    monkeypatch.setattr(analysis_service, "analyze_text", fake_analyze_text)
    monkeypatch.setattr(analysis_service, "save_analysis", fake_save_analysis)

    result = analysis_service.create_analysis("Hello world")

    assert result == {"analysis": "Test analysis"}
    assert saved["input_text"] == "Hello world"
    assert saved["analysis"] == "Test analysis"
    assert saved["source_type"] == "manual"
    assert saved["source_name"] is None


def test_create_analysis_success_file_metadata(monkeypatch):
    saved = {}

    def fake_analyze_text(text):
        return {"analysis": "File analysis"}

    def fake_save_analysis(input_text, analysis, source_type="manual", source_name=None):
        saved["input_text"] = input_text
        saved["analysis"] = analysis
        saved["source_type"] = source_type
        saved["source_name"] = source_name

    monkeypatch.setattr(analysis_service, "analyze_text", fake_analyze_text)
    monkeypatch.setattr(analysis_service, "save_analysis", fake_save_analysis)

    result = analysis_service.create_analysis(
        "Content from file",
        source_type="file",
        source_name="notes.txt"
    )

    assert result == {"analysis": "File analysis"}
    assert saved["input_text"] == "Content from file"
    assert saved["analysis"] == "File analysis"
    assert saved["source_type"] == "file"
    assert saved["source_name"] == "notes.txt"


def test_create_analysis_error(monkeypatch):
    def fake_analyze_text(text):
        return {"error": "Empty text not allowed"}

    monkeypatch.setattr(analysis_service, "analyze_text", fake_analyze_text)

    with pytest.raises(HTTPException) as exc_info:
        analysis_service.create_analysis("")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Empty text not allowed"


def test_list_analyses(monkeypatch):
    fake_analyses = [
        {
            "id": 1,
            "input_text": "Hello",
            "analysis": "Test",
            "source_type": "manual",
            "source_name": None,
            "created_at": "2026-03-16T12:00:00"
        }
    ]

    def fake_get_all_analyses(limit, offset):
        return fake_analyses

    monkeypatch.setattr(analysis_service, "get_all_analyses", fake_get_all_analyses)

    result = analysis_service.list_analyses(5, 0)

    assert result == fake_analyses


def test_get_analysis_found(monkeypatch):
    fake_analysis = {
        "id": 1,
        "input_text": "Hello",
        "analysis": "Test",
        "source_type": "manual",
        "source_name": None,
        "created_at": "2026-03-16T12:00:00"
    }

    def fake_get_analysis_by_id(analysis_id):
        return fake_analysis

    monkeypatch.setattr(analysis_service, "get_analysis_by_id", fake_get_analysis_by_id)

    result = analysis_service.get_analysis(1)

    assert result == fake_analysis


def test_get_analysis_not_found(monkeypatch):
    def fake_get_analysis_by_id(analysis_id):
        return None

    monkeypatch.setattr(analysis_service, "get_analysis_by_id", fake_get_analysis_by_id)

    with pytest.raises(HTTPException) as exc_info:
        analysis_service.get_analysis(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Analyse nicht gefunden"


def test_delete_analysis_by_id_success(monkeypatch):
    deleted = {}

    def fake_get_analysis_by_id(analysis_id):
        return {"id": analysis_id}

    def fake_delete_analysis(analysis_id):
        deleted["id"] = analysis_id

    monkeypatch.setattr(analysis_service, "get_analysis_by_id", fake_get_analysis_by_id)
    monkeypatch.setattr(analysis_service, "delete_analysis", fake_delete_analysis)

    result = analysis_service.delete_analysis_by_id(7)

    assert result == {"message": "Analysis deleted"}
    assert deleted["id"] == 7


def test_delete_analysis_by_id_not_found(monkeypatch):
    def fake_get_analysis_by_id(analysis_id):
        return None

    monkeypatch.setattr(analysis_service, "get_analysis_by_id", fake_get_analysis_by_id)

    with pytest.raises(HTTPException) as exc_info:
        analysis_service.delete_analysis_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Analyse nicht gefunden"