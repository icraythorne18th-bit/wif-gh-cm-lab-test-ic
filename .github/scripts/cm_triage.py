import json, sys, os

if len(sys.argv) < 2: sys.exit(1)

try:
    with open(sys.argv[1], 'r') as f: data = json.load(f)
except Exception: sys.exit(1)

findings = data.get('findings', []) if isinstance(data, dict) else data
if not isinstance(findings, list): findings = []

severities = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
max_sev_value, max_sev_name, high_critical_count = 0, "NONE", 0
fix_ids = []

for finding in findings:
    sev = finding.get('Severity', finding.get('severity', 'LOW')).upper()
    fid = finding.get('FindingID', finding.get('id', ''))
    if fid: fix_ids.append(fid)
    if severities.get(sev, 0) > max_sev_value:
        max_sev_value, max_sev_name = severities.get(sev, 0), sev
    if sev in ["CRITICAL", "HIGH"]: high_critical_count += 1

with open(os.environ.get('GITHUB_OUTPUT', 'output.txt'), 'a') as f:
    f.write(f"fix_ids={' '.join(fix_ids)}\n")
    f.write(f"max_severity={max_sev_name}\n")
    f.write(f"high_critical={high_critical_count}\n")

print(f"Triage complete. Max severity: {max_sev_name}")
