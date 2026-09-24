import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_and_readiness():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

        res_ready = await ac.get("/ready")
        assert res_ready.status_code == 200
        assert res_ready.json()["status"] == "ready"

@pytest.mark.asyncio
async def test_auth_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register new user
        reg_payload = {
            "email": "tester@breakthecode.dev",
            "password": "TestPassword123!",
            "full_name": "Test Candidate"
        }
        res_reg = await ac.post("/api/v1/auth/register", json=reg_payload)
        # Should be 201 or 400 if already exists
        if res_reg.status_code == 201:
            data = res_reg.json()
            assert "access_token" in data
            assert data["user"]["email"] == "tester@breakthecode.dev"

        # Login
        login_payload = {
            "email": "tester@breakthecode.dev",
            "password": "TestPassword123!"
        }
        res_login = await ac.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        token = res_login.json()["access_token"]

        # Fetch profile
        headers = {"Authorization": f"Bearer {token}"}
        res_me = await ac.get("/api/v1/users/me", headers=headers)
        assert res_me.status_code == 200
        assert res_me.json()["email"] == "tester@breakthecode.dev"

@pytest.mark.asyncio
async def test_technologies_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/technologies")
        assert res.status_code == 200
        techs = res.json()
        assert len(techs) >= 3
        tech_slugs = [t["slug"] for t in techs]
        assert "langgraph" in tech_slugs
        assert "java-backend" in tech_slugs

@pytest.mark.asyncio
async def test_questions_list_and_filter():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # All questions
        res = await ac.get("/api/v1/questions")
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["total"] >= 10
        assert len(data["items"]) >= 1

        # Filter by difficulty
        res_diff = await ac.get("/api/v1/questions?difficulty=TOUGH")
        assert res_diff.status_code == 200
        items_diff = res_diff.json()["items"]
        for item in items_diff:
            assert item["difficulty"] == "TOUGH"

@pytest.mark.asyncio
async def test_question_detail_and_think_mode():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_list = await ac.get("/api/v1/questions?limit=1")
        assert res_list.status_code == 200
        slug = res_list.json()["items"][0]["slug"]
        res = await ac.get(f"/api/v1/questions/{slug}")
        assert res.status_code == 200
        payload = res.json()["data"]
        assert payload["slug"] == slug
        assert len(payload["hints"]) == 3
        assert payload["interview_ready_answer"] is not None
        assert payload["code_example"] is not None
        assert len(payload["sources"]) >= 1

@pytest.mark.asyncio
async def test_search_and_autocomplete():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/search?q=LangGraph")
        assert res.status_code == 200
        results = res.json()["results"]
        assert len(results) >= 1

        res_auto = await ac.get("/api/v1/search/autocomplete?q=Lang")
        assert res_auto.status_code == 200
        assert "questions" in res_auto.json()["suggestions"]

@pytest.mark.asyncio
async def test_ai_answer_evaluation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        eval_payload = {
            "question_id": "langgraph-checkpointing-state-persistence",
            "candidate_answer": (
                "Checkpointing in LangGraph saves graph state after each superstep into a database "
                "like Postgres using AsyncPostgresSaver. When workers crash, they restore state using thread_id."
            ),
            "time_spent_seconds": 95
        }
        res = await ac.post("/api/v1/ai/evaluate-answer", json=eval_payload)
        assert res.status_code == 200
        eval_data = res.json()
        assert eval_data["overall_score"] >= 6.0
        assert "correctness" in eval_data
        assert len(eval_data["covered_points"]) >= 1
        assert len(eval_data["missed_points"]) >= 1

@pytest.mark.asyncio
async def test_rbac_guard():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Candidate login (regular user)
        res_user_login = await ac.post("/api/v1/auth/login", json={
            "email": "candidate@breakthecode.dev",
            "password": "CandidatePass123!"
        })
        assert res_user_login.status_code == 200
        user_token = res_user_login.json()["access_token"]

        # Candidate attempting admin endpoint -> 403 Forbidden
        res_forbidden = await ac.get("/api/v1/admin/analytics", headers={"Authorization": f"Bearer {user_token}"})
        assert res_forbidden.status_code == 403

        # Admin login
        res_admin_login = await ac.post("/api/v1/auth/login", json={
            "email": "admin@breakthecode.dev",
            "password": "AdminPass123!"
        })
        assert res_admin_login.status_code == 200
        admin_token = res_admin_login.json()["access_token"]

        # Admin accessing admin endpoint -> 200 OK
        res_admin = await ac.get("/api/v1/admin/analytics", headers={"Authorization": f"Bearer {admin_token}"})
        assert res_admin.status_code == 200
        assert res_admin.json()["metrics"]["total_questions"] >= 30

@pytest.mark.asyncio
async def test_gamification_and_dashboard_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register a fresh candidate
        email = f"learner_{id(ac)}@breakthecode.dev"
        res_reg = await ac.post("/api/v1/auth/register", json={
            "email": email,
            "password": "LearnerPass123!",
            "full_name": "Active Learner"
        })
        assert res_reg.status_code == 201
        token = res_reg.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Fetch initial dashboard
        res_dash = await ac.get("/api/v1/users/dashboard", headers=headers)
        assert res_dash.status_code == 200
        dash_data = res_dash.json()
        assert dash_data["total_xp"] == 0
        assert dash_data["total_attempted"] == 0
        assert len(dash_data["badges"]) >= 5

        # 2. Bookmark a question
        res_list = await ac.get("/api/v1/questions?limit=1")
        assert res_list.status_code == 200
        q_slug = res_list.json()["items"][0]["slug"]
        res_q = await ac.get(f"/api/v1/questions/{q_slug}")
        assert res_q.status_code == 200
        q_id = res_q.json()["data"]["id"]
        res_bm = await ac.post(f"/api/v1/questions/{q_id}/bookmark", headers=headers)
        assert res_bm.status_code == 200
        assert res_bm.json()["bookmarked"] is True

        # Check bookmarks list
        res_bms = await ac.get("/api/v1/users/bookmarks", headers=headers)
        assert res_bms.status_code == 200
        assert res_bms.json()["total"] == 1
        assert res_bms.json()["items"][0]["question_id"] == q_id

        # 3. Submit an answer for evaluation with auth header
        eval_payload = {
            "question_id": q_id,
            "candidate_answer": (
                "LangGraph state persistence works through checkpointer interfaces such as AsyncPostgresSaver. "
                "Every superstep atomically commits the graph state channel dictionary, allowing fault tolerance and human in the loop."
            ),
            "time_spent_seconds": 75
        }
        res_eval = await ac.post("/api/v1/ai/evaluate-answer", json=eval_payload, headers=headers)
        assert res_eval.status_code == 200
        eval_resp = res_eval.json()
        assert eval_resp["xp_earned"] >= 50
        assert eval_resp["streak_days"] >= 1
        assert eval_resp["srs_interval_days"] is not None

        # 4. Verify updated dashboard reflection
        res_dash2 = await ac.get("/api/v1/users/dashboard", headers=headers)
        assert res_dash2.status_code == 200
        dash2 = res_dash2.json()
        assert dash2["total_attempted"] == 1
        assert dash2["total_xp"] >= 50
        assert dash2["streak_days"] == 1
        assert len(dash2["recent_attempts"]) == 1

        # 5. Check SRS revision queue & submit review
        res_srs = await ac.get("/api/v1/users/revision", headers=headers)
        assert res_srs.status_code == 200
        srs_items = res_srs.json()["items"]
        assert len(srs_items) == 1
        assert srs_items[0]["question_id"] == q_id

        # Manual SRS review rating (4: Great)
        res_rev = await ac.post(f"/api/v1/users/revision/{q_id}/review", json={"grade": 4}, headers=headers)
        assert res_rev.status_code == 200
        assert res_rev.json()["card"]["repetitions"] >= 1

        # 6. Check badges
        res_badges = await ac.get("/api/v1/users/badges", headers=headers)
        assert res_badges.status_code == 200
        assert res_badges.json()["unlocked_count"] >= 1

        # 7. Check daily challenge
        res_dc = await ac.get("/api/v1/users/daily-challenge", headers=headers)
        assert res_dc.status_code == 200
        assert "challenge" in res_dc.json()

