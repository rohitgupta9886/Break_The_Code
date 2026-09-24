import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_reading_mode_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/questions/reading-mode/langgraph")
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert "technology" in data
        assert data["technology"]["slug"] == "langgraph"
        assert "summary" in data
        assert data["summary"]["total_questions"] > 0
        assert "tiers" in data
        assert len(data["tiers"]) > 0

        # Check tier structure
        first_tier = data["tiers"][0]
        assert "tier" in first_tier
        assert "level_code" in first_tier
        assert "label" in first_tier
        assert "experience_range" in first_tier
        assert "questions" in first_tier
        assert len(first_tier["questions"]) > 0

        # Check question structure inside tier
        q = first_tier["questions"][0]
        assert "id" in q
        assert "slug" in q
        assert "title" in q
        assert q["title"].endswith("?")
        assert "interview_ready_answer" in q
        assert "code_example" in q

        # Verify quality gates: all questions must be PUBLISHED and have an answer
        for tier in data["tiers"]:
            for question in tier["questions"]:
                assert question["status"] == "PUBLISHED"
                has_answer = bool(
                    question.get("interview_ready_answer")
                    or question.get("short_answer")
                    or question.get("deep_explanation")
                )
                assert has_answer, f"Question {question['slug']} missing answer content"

        # Verify difficulty tiers are ordered deterministically
        expected_tier_order = [
            "BASIC",
            "MEDIUM",
            "HARD",
            "TOUGH",
            "VERY_TOUGH",
            "VERY_VERY_TOUGH",
            "PRODUCTION_SCENARIO",
            "EXPERT_DEEP_DIVE",
        ]
        tier_names = [t["tier"] for t in data["tiers"]]
        # Ensure that every tier found appears in the order of expected_tier_order
        indices = [expected_tier_order.index(name) for name in tier_names if name in expected_tier_order]
        assert indices == sorted(indices), "Tiers must be strictly ordered from BASIC to EXPERT_DEEP_DIVE"

@pytest.mark.asyncio
async def test_reading_mode_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/questions/reading-mode/non-existent-tech-xyz")
        assert res.status_code == 404

