import re

def clean_concept_name(text: str) -> str:
    """
    Strips question prefixes, interrogatives, and technology qualifiers
    so that the remaining concept name can be cleanly embedded in answers.
    e.g. 'What is the foundational role of Core Internal Mechanics & State Transition in LangGraph & Agentic AI, and how does it operate?'
    -> 'Core Internal Mechanics & State Transition'
    """
    s = text.strip()
    
    # Common prefixes to strip
    prefixes = [
        r"^what is the foundational role of\s+",
        r"^what is the role of\s+",
        r"^what is\s+",
        r"^what are\s+",
        r"^how do you identify and resolve performance bottlenecks and concurrency trade-offs of\s+",
        r"^how do you identify and mitigate the performance bottlenecks and concurrency trade-offs of\s+",
        r"^how do you implement and optimize\s+",
        r"^how do you optimize and debug\s+",
        r"^how do you architect, scale, and ensure fault tolerance for\s+",
        r"^how do you\s+",
        r"^how does\s+",
        r"^how would you architect a globally resilient\s+[A-Za-z0-9\s&]+platform handling 100k requests/sec while strictly guaranteeing\s+",
        r"^how to\s+",
        r"^why are\s+",
        r"^why is\s+",
        r"^why does\s+",
        r"^explain\s+"
    ]
    for p in prefixes:
        s = re.sub(p, "", s, flags=re.IGNORECASE)
        
    # Strip common suffixes
    suffixes = [
        r",\s*and how does it operate\??$",
        r",\s*and how is it implemented\??$",
        r",\s*and what failure modes must you mitigate\??$",
        r",\s*and what are its exact Time and Space complexities\??$",
        r",\s*and how do you handle complex edge cases\??$",
        r"\s+in [A-Za-z0-9\s&]+ architectures\??$",
        r"\s+in [A-Za-z0-9\s&]+ systems\??$",
        r"\s+in [A-Za-z0-9\s&]+\??$",
        r"\?+$"
    ]
    for suf in suffixes:
        s = re.sub(suf, "", s, flags=re.IGNORECASE)
        
    s = s.strip()
    return s if s else text
