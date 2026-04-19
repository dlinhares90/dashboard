import urllib.request, json, os, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = open('.env').read().split('KOMMO_ACCESS_TOKEN=')[1].split('\n')[0].strip()
DOMAIN = 'arthurdiasimplantodontista.kommo.com'

def fetch(path):
    req = urllib.request.Request(f'https://{DOMAIN}/api/v4{path}',
                                 headers={'Authorization': f'Bearer {TOKEN}'})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Fetch ALL leads paginating
all_leads = []
page = 1
while True:
    data = fetch(f'/leads?limit=250&page={page}')
    batch = data.get('_embedded', {}).get('leads', [])
    if not batch:
        break
    all_leads.extend(batch)
    if 'next' not in data.get('_links', {}):
        break
    page += 1

print(f'Total leads na API: {len(all_leads)}')
print(f'Total páginas: {page}')

# Count by status_id
status_counts = Counter(l['status_id'] for l in all_leads)
pipeline_counts = Counter(l['pipeline_id'] for l in all_leads)

print(f'\nPipelines encontrados: {dict(pipeline_counts)}')

# Get pipeline names
pipelines = fetch('/leads/pipelines')
pipe_names = {}
stage_names = {}
for p in pipelines['_embedded']['pipelines']:
    pipe_names[p['id']] = p['name']
    for s in p['_embedded']['statuses']:
        stage_names[s['id']] = f"{p['name']} → {s['name']}"

# Add default won/lost
stage_names[142] = 'Ganha (global)'
stage_names[143] = 'Perdida (global)'

print('\nPipelines:')
for pid, count in pipeline_counts.most_common():
    print(f'  {pipe_names.get(pid, pid)}: {count} leads')

print('\nTop 15 etapas:')
for sid, count in status_counts.most_common(15):
    print(f'  {sid} | {count:5d} | {stage_names.get(sid, "???")}')

# Total value
total_value = sum(l.get('price', 0) or 0 for l in all_leads)
print(f'\nValor total: R$ {total_value:,.2f}')
