import asyncio
import os
import sys

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.core.config import settings
from app.services.ai_service import get_llm_provider, GeminiLLMProvider


async def run_verification():
    print("=" * 60)
    print("   BREAK THE CODE - GOOGLE GEMINI PRODUCTION INTEGRATION TEST")
    print("=" * 60)

    # 1. Environment & Configuration Check
    api_key = settings.get_gemini_api_key()
    provider_type = settings.LLM_PROVIDER
    model = settings.GEMINI_MODEL

    print(f"\n[1] Configuration Check:")
    print(f"  - Provider: {provider_type}")
    print(f"  - Model: {model}")
    masked_key = f"{api_key[:6]}...{api_key[-4:]}" if api_key else "MISSING"
    print(f"  - Resolved API Key: {masked_key}")

    if not api_key:
        print("ERROR: No Google Gemini API key resolved from environment.")
        return False

    # 2. Provider Initialization Check
    print(f"\n[2] Provider Factory Test:")
    provider = get_llm_provider()
    print(f"  - Instantiated Provider: {provider.__class__.__name__}")
    if not isinstance(provider, GeminiLLMProvider):
        print("WARNING: Expected GeminiLLMProvider but got a different provider.")

    # 3. Dynamic Socratic Hint Generation
    print(f"\n[3] Testing Real Gemini Socratic Hint Generation:")
    sample_question = "How does LangGraph manage state persistence across multi-turn human-in-the-loop cycles?"
    candidate_draft = "I think it saves state in memory or SQLite, but not sure how checkpoints work when interrupted."
    
    hint_result = await provider.generate_hint(
        question=sample_question,
        candidate_thought=candidate_draft,
        level=2
    )
    print(f"  - Hint Level: {hint_result.get('hint_level')} ({hint_result.get('hint_type')})")
    print(f"  - Socratic Question: {hint_result.get('socratic_question')}")
    print(f"  - Guiding Clue: {hint_result.get('guiding_clue')}")

    assert hint_result.get("socratic_question"), "Socratic question must not be empty"

    # 4. Structured Technical Answer Evaluation
    print(f"\n[4] Testing Real Gemini Structured Technical Answer Evaluation:")
    ideal_answer = (
        "LangGraph implements checkpoint savers (e.g. MemorySaver, AsyncSqliteSaver, PostgresSaver). "
        "Each superstep produces a thread-scoped snapshot identified by thread_id and checkpoint_id. "
        "During human-in-the-loop interrupts, execution suspends, state is serialized, and when resumed, "
        "the state graph loads the latest checkpoint or can travel back to a previous checkpoint via update_state."
    )
    candidate_answer = (
        "LangGraph uses thread_id to track conversations. When interrupted, it saves the state to a database saver. "
        "When the human approves or edits the state, it continues from where it left off."
    )

    eval_result = await provider.evaluate_response(
        question=sample_question,
        ideal_answer=ideal_answer,
        candidate_answer=candidate_answer
    )

    print(f"  - Overall Score: {eval_result.get('overall_score')}/10")
    print(f"  - Correctness: {eval_result.get('correctness', {}).get('score')}/10 - {eval_result.get('correctness', {}).get('feedback')}")
    print(f"  - Technical Depth: {eval_result.get('technical_depth', {}).get('score')}/10 - {eval_result.get('technical_depth', {}).get('feedback')}")
    print(f"  - Points Covered ({len(eval_result.get('covered_points', []))}): {eval_result.get('covered_points')}")
    print(f"  - Points Missed ({len(eval_result.get('missed_points', []))}): {eval_result.get('missed_points')}")
    print(f"  - Principal Advice: {eval_result.get('actionable_advice')}")

    assert eval_result.get("overall_score") is not None, "Overall score must be present"
    assert "correctness" in eval_result, "Correctness metric must be present"
    assert "improved_answer" in eval_result, "Improved answer must be present"

    # 5. Real-Time Streaming Test
    print(f"\n[5] Testing Real Gemini Real-Time Token Streaming:")
    token_count = 0
    stream_sample = ""
    async for chunk in provider.stream_evaluation(
        question=sample_question,
        ideal_answer=ideal_answer,
        candidate_answer=candidate_answer
    ):
        token_count += 1
        stream_sample += chunk
        if token_count <= 8:
            print(f"    stream chunk #{token_count}: {repr(chunk)}")

    print(f"  - Total Streamed Characters: {len(stream_sample)}")
    print(f"  - Stream Sample: {stream_sample[:120]}...")

    print("\n" + "=" * 60)
    print("   ALL GOOGLE GEMINI PRODUCTION API TESTS PASSED!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = asyncio.run(run_verification())
    sys.exit(0 if success else 1)
