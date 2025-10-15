from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)

TEST_ACTIVITY = "Programming Class"
TEST_EMAIL = "testuser@example.com"


def setup_function():
    # Ensure test email is not present before each test
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)


def teardown_function():
    # Clean up after tests
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert TEST_ACTIVITY in data


def test_signup_and_duplicate():
    # Signup should succeed
    resp = client.post(f"/activities/{TEST_ACTIVITY}/signup?email={TEST_EMAIL}")
    assert resp.status_code == 200
    assert TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]

    # Duplicate signup should fail with 400
    resp2 = client.post(f"/activities/{TEST_ACTIVITY}/signup?email={TEST_EMAIL}")
    assert resp2.status_code == 400


def test_delete_participant_and_not_found():
    # Ensure participant exists
    if TEST_EMAIL not in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].append(TEST_EMAIL)

    # Delete participant
    resp = client.delete(f"/activities/{TEST_ACTIVITY}/participants?email={TEST_EMAIL}")
    assert resp.status_code == 200
    assert TEST_EMAIL not in activities[TEST_ACTIVITY]["participants"]

    # Deleting again should return 404
    resp2 = client.delete(f"/activities/{TEST_ACTIVITY}/participants?email={TEST_EMAIL}")
    assert resp2.status_code == 404