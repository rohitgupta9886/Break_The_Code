from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import AIService
from app.schemas.ai import (
    AnswerEvaluationRequest,
    AnswerEvaluationResponse,
    SocraticHintRequest,
    SocraticHintResponse
)

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/evaluate-answer", response_model=AnswerEvaluationResponse)
async def evaluate_answer(
    request: AnswerEvaluationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Submits candidate answer for comprehensive Google Gemini technical evaluation,
    returning scored rubrics, covered/missed points, improved answer, and gamification rewards.
    """
    service = AIService(db)
    user_id = current_user.id if current_user else None
    result = await service.evaluate_answer(request, user_id=user_id)
    return result

@router.post("/evaluate-answer/stream")
async def stream_evaluate_answer(
    request: AnswerEvaluationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Streams a live AI architectural critique using Server-Sent Events (SSE)
    powered by Google Gemini's native streaming capabilities.
    """
    service = AIService(db)

    async def event_generator():
        async for chunk in service.stream_evaluation(request):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/socratic-hint", response_model=SocraticHintResponse)
async def get_socratic_hint(
    request: SocraticHintRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generates an adaptive Socratic hint powered by Google Gemini, tailored
    to the specific question and candidate's thought process.
    """
    service = AIService(db)
    result = await service.generate_socratic_hint(request)
    return result
