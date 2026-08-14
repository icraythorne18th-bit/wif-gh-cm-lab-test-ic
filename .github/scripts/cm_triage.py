import json
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 cm_triage.py <path_to_report.json>")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading report: {e}")
    sys.exit(1)

findings = data.get('findings', []) if isinstance(data, dict) else data
if not isinstance(findings, list): findings = []

severities = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
max_sev_value, max_sev_name = 0, "NONE"
fix_ids = []

for finding in findings:
    sev = finding.get('severity', 'LOW').upper()
    fid = finding.get('id', '')
    if fid: fix_ids.append(fid)
    if severities.get(sev, 0) > max_sev_value:
        max_sev_value, max_sev_name = severities.get(sev, 0), sev

with open(os.environ.get('GITHUB_OUTPUT', 'output.txt'), 'a') as f:
    f.write(f"fix_ids={' '.join(fix_ids)}\n")
    f.write(f"max_severity={max_sev_name}\n")

print(f"Triage complete. Max severity: {max_sev_name}")
