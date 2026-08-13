from __future__ import annotations
import re
from epifair.schema import EpistemicAction

PATTERNS={
 EpistemicAction.CLARIFY:[r"could you (?:clarify|provide|tell me)",r"need more information",r"what .* do you mean"],
 EpistemicAction.CHECK:[r"verify",r"check (?:the|this|with)",r"look up",r"consult (?:a|the)"],
 EpistemicAction.ABSTAIN:[r"cannot determine",r"can't determine",r"not enough information to (?:answer|determine)",r"i don't know"],
 EpistemicAction.REFUSE:[r"i (?:can't|cannot|won't) help with",r"i must refuse",r"not able to assist"],
}

def classify_action(text: str) -> tuple[EpistemicAction,float,str]:
    t=text.lower(); hits=[]
    for action,pats in PATTERNS.items():
        if any(re.search(p,t) for p in pats): hits.append(action)
    if EpistemicAction.REFUSE in hits: return EpistemicAction.REFUSE,0.95,"rule_refusal"
    if EpistemicAction.CLARIFY in hits: return EpistemicAction.CLARIFY,0.9,"rule_clarify"
    if EpistemicAction.CHECK in hits: return EpistemicAction.CHECK,0.85,"rule_check"
    if EpistemicAction.ABSTAIN in hits: return EpistemicAction.ABSTAIN,0.85,"rule_abstain"
    return EpistemicAction.ANSWER,0.55,"rule_default_answer"
