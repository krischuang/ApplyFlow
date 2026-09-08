def test_list_empty(client):
    resp = client.get("/api/v1/applications")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_defaults_status_to_saved(client):
    resp = client.post("/api/v1/applications", json={"job_title": "Backend Engineer", "company_name": "Acme"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "SAVED"
    assert body["auto_applied"] is False


def test_create_and_get_one(client):
    created = client.post("/api/v1/applications", json={"job_title": "SWE", "company_name": "Acme"}).json()

    resp = client.get(f"/api/v1/applications/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["job_title"] == "SWE"


def test_get_missing_returns_404(client):
    resp = client.get("/api/v1/applications/999999")
    assert resp.status_code == 404


def test_list_filters_by_status(client):
    client.post("/api/v1/applications", json={"job_title": "A", "company_name": "X", "status": "SAVED"})
    client.post("/api/v1/applications", json={"job_title": "B", "company_name": "Y", "status": "APPLIED"})

    resp = client.get("/api/v1/applications", params={"status": "APPLIED"})
    assert resp.status_code == 200
    titles = [a["job_title"] for a in resp.json()]
    assert titles == ["B"]


def test_update_partial_fields_only(client):
    created = client.post("/api/v1/applications", json={"job_title": "SWE", "company_name": "Acme"}).json()

    resp = client.put(f"/api/v1/applications/{created['id']}", json={"notes": "Great culture fit"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["notes"] == "Great culture fit"
    assert body["job_title"] == "SWE"  # untouched


def test_update_missing_returns_404(client):
    resp = client.put("/api/v1/applications/999999", json={"notes": "x"})
    assert resp.status_code == 404


def test_update_status_endpoint(client):
    created = client.post("/api/v1/applications", json={"job_title": "SWE", "company_name": "Acme"}).json()

    resp = client.patch(f"/api/v1/applications/{created['id']}/status", params={"status": "INTERVIEWING"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "INTERVIEWING"


def test_delete_application(client):
    created = client.post("/api/v1/applications", json={"job_title": "SWE", "company_name": "Acme"}).json()

    resp = client.delete(f"/api/v1/applications/{created['id']}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/applications/{created['id']}")
    assert resp.status_code == 404


def test_delete_missing_returns_404(client):
    resp = client.delete("/api/v1/applications/999999")
    assert resp.status_code == 404
