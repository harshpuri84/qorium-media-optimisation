"""Retrieve public references with pinned provenance; never overwrite changed raw files."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
MANIFEST = RAW / 'source_manifest.json'


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Qorium-case-study-data-preparation'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())
        for item in manifest['files']:
            path = ROOT / item['path']
            # Reference files from the Cosenza repository are not redistributed and no analysis reads them;
            # download them only when asked (FETCH_REFERENCE=1).
            if 'cosenza_2022' in item['path'] and not path.exists() and not os.environ.get('FETCH_REFERENCE'):
                continue
            if path.exists():
                if sha(path.read_bytes()) != item['sha256']:
                    raise ValueError(f'Raw file changed: {path}')
            else:
                data = get(item['url'])
                if sha(data) != item['sha256']:
                    raise ValueError(f'Remote source changed: {item["url"]}')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        print('Verified retained source files (Cosenza reference files skipped unless FETCH_REFERENCE=1).')
        return

    metadata_bytes = get('https://api.figshare.com/v2/articles/27715134')
    metadata = json.loads(metadata_bytes)
    repo = 'ZacharyCosenza/GradStuff_Cosenza'
    commit = json.loads(get(f'https://api.github.com/repos/{repo}/commits/main'))['sha']
    sources = [(f'data/raw/narayanan_2025/{f["name"]}', f['download_url'],
                'Narayanan et al. 2025', 'MIT', None) for f in metadata['files']]
    for name in ['README.md', 'DBO_Solver.py', 'torchtoolbox.py',
                 'DBO_Data/BO_data.txt', 'DBO_Data/BO_outputs.txt']:
        sources.append((f'data/raw/cosenza_2022/{Path(name).name}',
                        f'https://raw.githubusercontent.com/{repo}/{commit}/{name}',
                        'Cosenza reference repository; semantics not verified',
                        'Check repository licensing before redistribution', None))
    sources.append(('data/raw/narayanan_2025/metadata.json',
                    'https://api.figshare.com/v2/articles/27715134',
                    'Figshare article metadata', 'MIT dataset metadata', metadata_bytes))
    records = []
    for relative, url, citation, licence, payload in sources:
        data = payload if payload is not None else get(url)
        path = ROOT / relative
        # An existing metadata JSON may have different whitespace; preserve the
        # freshly retrieved bytes only on first provenance registration.
        if path.exists() and path.name != 'metadata.json' and sha(path.read_bytes()) != sha(data):
            raise ValueError(f'Existing source does not match pinned download: {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.name == 'metadata.json':
            path.write_bytes(data)
        records.append({'path': relative, 'url': url, 'sha256': sha(data),
                        'bytes': len(data), 'citation': citation, 'licence': licence,
                        'retrieved_at_utc': datetime.now(timezone.utc).isoformat()})
    MANIFEST.write_text(json.dumps({'figshare_article': 27715134,
                                   'github_commit': commit, 'files': records}, indent=2) + '\n')
    print(f'Registered {len(records)} files with SHA256 provenance.')


if __name__ == '__main__':
    main()
