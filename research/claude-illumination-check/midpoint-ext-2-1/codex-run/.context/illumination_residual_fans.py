"""Load immutable first-fan results and expose their unresolved branches."""
import json
from classify_illumination_three_exception import OUT,digest
from search_illumination_fan_partitions import TARGET,CELL,load_seed,fan_masks,fix_fan
from search_illumination_cell_partitions import fix_cells
from search_illumination_three_two_star import add_guard

SECOND_CELL=(1,1)

def load_residual():
    model,ts,x,bounded,terms,keys,_,provenance=load_seed()
    path=OUT/'fan-search-2-1.json';saved=json.loads(path.read_text())
    receipt_path=OUT/'fan-audit-2-1.json';receipt=json.loads(receipt_path.read_text())
    assert receipt['status']=='PASS' and receipt['source_sha256']==digest(path)
    assert saved['provenance']==provenance
    for record in saved['records']:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']));assert key not in keys
            keys.add(key);add_guard(model,x,guard['tile_facts'])
    ids,masks=fan_masks(ts)
    residual=[(tuple(map(tuple,c['outside_cells'])),c['mask']) for c in receipt['classes'] if c['status']!='INFEASIBLE']
    assert len(residual)==18 and all(mask in masks for _,mask in residual)
    provenance=dict(parent=provenance,fan_search_sha256=digest(path),fan_audit_sha256=digest(receipt_path))
    return model,ts,x,bounded,terms,keys,ids,residual,provenance

def fix_first(model,terms,bounded,x,ids,outside,mask):
    fix_cells(model,terms,bounded,outside);fix_fan(model,x,ids,mask)
