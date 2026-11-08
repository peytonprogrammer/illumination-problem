"""Bounded alternative one-pass search for three immutable saved rooms."""
from collections import Counter
import json,time
from classify_illumination_three_exception import BASE,OUT,digest
from search_illumination_midpoint_covers import one_pass,find_one_pass
from analyze_illumination_exception_itineraries import independent_events

SOURCE=BASE/'three-two-star/case-1-1.json'
PATH=OUT/'midpoint-probe-1-1.json'


def run():
    assert not PATH.exists()
    saved=json.loads(SOURCE.read_text());freq=Counter(tuple(r['witness']['direction']) for r in saved['records'] if len(independent_events(r['witness']))==1)
    library=[d for d,n in freq.most_common()];records=[];deadline=time.monotonic()+90
    for i,r in enumerate(saved['records']):
        if len(independent_events(r['witness']))==1:
            one_pass(r['room'],r['witness']);continue
        witness,screen=find_one_pass(r['room'],library,deadline)
        if witness:one_pass(r['room'],witness)
        records.append(dict(record_index=i,room=r['room'],witness=witness,screen=screen))
        print(json.dumps(dict(record_index=i,found=bool(witness),screen=screen)),flush=True)
    result=dict(source_sha256=digest(SOURCE),records=records,summary=dict(rooms=len(records),found=sum(bool(r['witness']) for r in records),unresolved=sum(not r['witness'] for r in records)),scope='Primitive directions through bound16 plus saved library; positive paths exact. Finite misses unresolved, never dark.')
    PATH.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary']),flush=True)


if __name__=='__main__':run()
