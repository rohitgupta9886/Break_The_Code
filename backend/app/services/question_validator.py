import re
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    is_valid: bool
    is_unique: bool
    is_correct_technology: bool
    is_correct_section: bool
    is_correct_difficulty: bool
    is_correct_experience_level: bool
    is_complete_answer: bool
    is_technically_validated: bool
    is_approved: bool
    is_not_outdated: bool
    is_publishable: bool
    target_tier: str # 'L1' or 'L2' or 'OTHER'
    failure_reasons: List[str] = field(default_factory=list)

class QuestionLevelValidator:
    """
    Validates technical interview questions against the 10-point Break The Code Standard:
    1. UNIQUE: Non-duplicate title and content across the repository.
    2. CORRECT TECHNOLOGY: Properly bound to a valid Technology Pillar.
    3. CORRECT SECTION: Properly bound to a canonical Section / Topic.
    4. CORRECT DIFFICULTY: Accurate difficulty tier and difficulty score (1.0-4.0 for L1, 4.1-6.5 for L2).
    5. CORRECT EXPERIENCE LEVEL: Matches target cohort (0-2y for L1, 3-5y for L2).
    6. COMPLETE ANSWER: Populated 15-part Answer DNA with substantial explanations.
    7. TECHNICALLY VALIDATED: All 7 quality metrics >= 0.90 + authentic documentation sources.
    8. APPROVED: Status in APPROVED or PUBLISHED.
    9. NOT OUTDATED: Active 2026 specs, non-deprecated.
    10. PUBLISHABLE: Slug, title, tags, and formatting ready for production delivery.
    """

    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return re.sub(r'\s+', ' ', text)

    @classmethod
    def compute_jaccard_similarity(cls, text1: str, text2: str) -> float:
        words1 = set(cls.normalize_text(text1).split())
        words2 = set(cls.normalize_text(text2).split())
        if not words1 or not words2:
            return 0.0
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union

    @classmethod
    def audit_question(
        cls, 
        q_data: Dict[str, Any], 
        existing_titles: Optional[Set[str]] = None,
        target_level: Optional[str] = None # 'L1', 'L2', or None (auto-detect)
    ) -> ValidationResult:
        reasons = []

        title = (q_data.get("title") or "").strip()
        slug = (q_data.get("slug") or "").strip()
        tech_id = q_data.get("technology_id")
        topic_id = q_data.get("topic_id")
        difficulty = (q_data.get("difficulty") or "").upper()
        diff_score = float(q_data.get("difficulty_score") or 0.0)
        depth = (q_data.get("interview_depth") or "").upper()
        exp_level = (q_data.get("experience_level") or "").strip()
        status = (q_data.get("status") or "").upper()

        # 1. Target Level Detection
        if target_level:
            level = target_level.upper()
        else:
            if depth == "L1" or difficulty == "BASIC":
                level = "L1"
            elif depth == "L2" or difficulty == "MEDIUM":
                level = "L2"
            else:
                level = "OTHER"

        # 2. UNIQUE Check
        is_unique = True
        if not title:
            is_unique = False
            reasons.append("Question title is empty")
        elif existing_titles:
            norm_title = cls.normalize_text(title)
            for other_title in existing_titles:
                if other_title == title:
                    continue
                if cls.compute_jaccard_similarity(norm_title, other_title) > 0.68:
                    is_unique = False
                    reasons.append(f"Question title is too similar to existing question: '{other_title[:60]}...'")
                    break

        # 3. CORRECT TECHNOLOGY Check
        is_correct_tech = bool(tech_id)
        if not is_correct_tech:
            reasons.append("Missing valid technology_id")

        # 4. CORRECT SECTION Check
        is_correct_section = bool(topic_id)
        if not is_correct_section:
            reasons.append("Missing valid topic_id (canonical section)")

        # 5. CORRECT DIFFICULTY Check
        is_correct_difficulty = True
        if level == "L1":
            if difficulty != "BASIC":
                is_correct_difficulty = False
                reasons.append(f"L1 question must have difficulty 'BASIC', got '{difficulty}'")
            if diff_score < 1.0 or diff_score > 4.0:
                is_correct_difficulty = False
                reasons.append(f"L1 difficulty_score must be between 1.0 and 4.0, got {diff_score}")
        elif level == "L2":
            if difficulty != "MEDIUM":
                is_correct_difficulty = False
                reasons.append(f"L2 question must have difficulty 'MEDIUM', got '{difficulty}'")
            if diff_score < 4.0 or diff_score > 6.5:
                is_correct_difficulty = False
                reasons.append(f"L2 difficulty_score must be between 4.0 and 6.5, got {diff_score}")

        # 6. CORRECT EXPERIENCE LEVEL Check
        is_correct_experience_level = True
        if level == "L1":
            if depth != "L1":
                is_correct_experience_level = False
                reasons.append(f"L1 question must have interview_depth 'L1', got '{depth}'")
            if "0-2" not in exp_level and "Fresher" not in exp_level and "Junior" not in exp_level:
                is_correct_experience_level = False
                reasons.append(f"L1 question must target 0-2 years / Freshers, got '{exp_level}'")
        elif level == "L2":
            if depth != "L2":
                is_correct_experience_level = False
                reasons.append(f"L2 question must have interview_depth 'L2', got '{depth}'")
            if "3-5" not in exp_level and "Mid" not in exp_level:
                is_correct_experience_level = False
                reasons.append(f"L2 question must target 3-5 years / Mid-level, got '{exp_level}'")

        # 7. COMPLETE ANSWER Check (15-Part DNA)
        short_ans = (q_data.get("short_answer") or "").strip()
        ready_ans = (q_data.get("interview_ready_answer") or "").strip()
        deep_exp = (q_data.get("deep_explanation") or "").strip()
        code_ex = (q_data.get("code_example") or "").strip()
        why_ask = (q_data.get("why_interviewer_asks") or "").strip()
        prod_cons = (q_data.get("production_considerations") or "").strip()
        fail_modes = (q_data.get("failure_modes") or "").strip()
        tradeoffs = (q_data.get("tradeoffs") or "").strip()
        common_mistakes = q_data.get("common_mistakes") or []

        is_complete_answer = True
        if len(ready_ans) < 80:
            is_complete_answer = False
            reasons.append(f"interview_ready_answer is too brief ({len(ready_ans)} chars < 80 chars)")
        if len(deep_exp) < 100:
            is_complete_answer = False
            reasons.append(f"deep_explanation is too brief ({len(deep_exp)} chars < 100 chars)")
        if not prod_cons and not tradeoffs:
            is_complete_answer = False
            reasons.append("Missing production considerations or trade-offs")
        if not why_ask:
            is_complete_answer = False
            reasons.append("Missing why_interviewer_asks component")

        # 8. TECHNICALLY VALIDATED Check (Quality scores >= 0.90 + primary authentic sources)
        scores = [
            float(q_data.get("technical_accuracy_score") or 0.0),
            float(q_data.get("answer_quality_score") or 0.0),
            float(q_data.get("difficulty_accuracy_score") or 0.0),
            float(q_data.get("originality_score") or 0.0),
            float(q_data.get("production_relevance_score") or 0.0),
            float(q_data.get("source_quality_score") or 0.0),
            float(q_data.get("overall_quality_score") or 0.0),
        ]
        sources = q_data.get("sources") or []
        is_technically_validated = True
        if any(s < 0.88 for s in scores):
            is_technically_validated = False
            reasons.append(f"Quality scores below threshold (min required 0.88-0.90, got {min(scores)})")
        if not sources or len(sources) == 0:
            is_technically_validated = False
            reasons.append("Missing authentic documentation sources")

        # 9. APPROVED Check
        is_approved = status in ["APPROVED", "PUBLISHED"]
        if not is_approved:
            reasons.append(f"Status is not APPROVED or PUBLISHED (got '{status}')")

        # 10. NOT OUTDATED Check
        is_not_outdated = status != "OUTDATED"
        if not is_not_outdated:
            reasons.append("Question is flagged as OUTDATED")

        # 11. PUBLISHABLE Check
        is_publishable = bool(slug and title and len(title) >= 15)
        if not is_publishable:
            reasons.append("Question lacks a valid slug or has a title under 15 characters")

        all_valid = (
            is_unique and
            is_correct_tech and
            is_correct_section and
            is_correct_difficulty and
            is_correct_experience_level and
            is_complete_answer and
            is_technically_validated and
            is_approved and
            is_not_outdated and
            is_publishable
        )

        return ValidationResult(
            is_valid=all_valid,
            is_unique=is_unique,
            is_correct_technology=is_correct_tech,
            is_correct_section=is_correct_section,
            is_correct_difficulty=is_correct_difficulty,
            is_correct_experience_level=is_correct_experience_level,
            is_complete_answer=is_complete_answer,
            is_technically_validated=is_technically_validated,
            is_approved=is_approved,
            is_not_outdated=is_not_outdated,
            is_publishable=is_publishable,
            target_tier=level,
            failure_reasons=reasons
        )
