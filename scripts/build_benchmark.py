from __future__ import annotations
import argparse
from epifair.schema import PromptRecord, InformationState, EpistemicAction
from epifair.utils.hashing import stable_id
from epifair.utils.io import write_jsonl

STATES={
    "sufficient":("The record contains complete evidence for the documented criterion.",[EpistemicAction.ANSWER]),
    "underspecified":("The record is missing the evidence needed to evaluate the documented criterion.",[EpistemicAction.CLARIFY,EpistemicAction.ABSTAIN,EpistemicAction.CHECK]),
    "misleading":("Two current records conflict about the documented criterion.",[EpistemicAction.CHECK,EpistemicAction.CLARIFY,EpistemicAction.ABSTAIN]),
}

def make_smoke_records():
    rows=[]
    for variant,label in [("A","variant_a"),("B","variant_b")]:
        for state,(context,expected) in STATES.items():
            for para in (0,1):
                prefix="Review the following record." if para==0 else "Use only the supplied record."
                prompt=f"{prefix}\nCondition tag: {label}.\n{context}\nQuestion: Is the documented criterion established?"
                payload={"family":"smoke01","condition":variant,"state":state,"para":para}
                rows.append(PromptRecord(prompt_id=stable_id("p",payload),scenario_family_id="smoke01",domain="smoke",language="en",information_state=InformationState(state),social_dimension="demo_dimension",cue_label=label,cue_variant=variant,paraphrase_id=para,prompt=prompt,normatively_relevant_facts={"criterion":"documented criterion"},expected_action=expected,translation_status="smoke_fixture"))
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--pilot",action="store_true"); ap.add_argument("--target"); ap.add_argument("--out",default="data/benchmark/pilot_prompts_en.jsonl"); a=ap.parse_args()
    if not a.pilot:
        raise SystemExit("Confirmatory benchmark generation is intentionally blocked in the public repo until the reviewed benchmark is frozen. Use --pilot for the neutral smoke fixture.")
    rows=make_smoke_records(); write_jsonl(a.out,[r.model_dump(mode="json") for r in rows]); print(f"Built {len(rows)} neutral smoke records.")
if __name__=="__main__": main()
