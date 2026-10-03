"""Configure a personal Desktop OAuth client locally, then upload DVC versions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('client_json', type=Path, help='Downloaded Google Desktop OAuth JSON file')
args = parser.parse_args()
with args.client_json.open(encoding='utf-8') as stream:
    client = json.load(stream).get('installed')
if not client or not client.get('client_id') or not client.get('client_secret'):
    parser.error('Expected an installed/Desktop OAuth client JSON document.')
if not Path('.dvc').is_dir():
    parser.error('Run this command from the repository root.')
Path('.secrets').mkdir(exist_ok=True)
for key, value in {
    'gdrive_client_id': client['client_id'],
    'gdrive_client_secret': client['client_secret'],
    'gdrive_user_credentials_file': str(Path('.secrets/drive-user.json').resolve()),
}.items():
    subprocess.run([sys.executable, '-m', 'dvc', 'remote', 'modify', '--local',
                    'gdrive_storage', key, value], check=True)
print('Client configured in ignored local settings. Complete Google consent in the browser.')
subprocess.run([sys.executable, '-m', 'dvc', 'push', '--all-branches', '--all-tags'], check=True)
