"""Build the privacy-clean representative-to-certificate index."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cert = ROOT / 'certificates'
representatives = json.loads((cert / 'cm_representative_cases.json').read_text())
records = []
for row in sorted(representatives, key=lambda r: (r['b'], r['rho'])):
    case_id = row['case_id']
    if case_id == 'b13_pair0':
        input_name, output_name = 'b13.json', 'b13_certificate.json'
    else:
        input_name = output_name = case_id + '.json'
    input_path = cert / 'cm_inputs' / input_name
    output_path = cert / 'cm_outputs' / output_name
    if not input_path.is_file() or not output_path.is_file():
        raise FileNotFoundError(case_id)
    records.append({
        'case_id': case_id,
        'input': 'certificates/cm_inputs/' + input_name,
        'certificate': 'certificates/cm_outputs/' + output_name,
    })
if len(records) != 27 or len({r['case_id'] for r in records}) != 27:
    raise ValueError('Expected 27 unique representative records')
(cert / 'cm_batch_results.json').write_text(json.dumps(records, indent=2) + '\n')
print('WROTE 27 privacy-clean representative bindings')

