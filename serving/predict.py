import os
import json
from pathlib import Path
import requests

def score_model(payload):
    host = os.environ['DATABRICKS_HOST'].rstrip('/')
    token = os.environ['DATABRICKS_TOKEN']
    response = requests.post(f'{host}/serving-endpoints/metrodemanda-serving/invocations', headers={'Authorization': f'Bearer {token}'}, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    payload = json.loads(Path(__file__).with_name('sample_request.json').read_text(encoding='utf-8'))
    print(json.dumps(score_model(payload), ensure_ascii=False, indent=2))
