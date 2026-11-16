import json
import os
import urllib.request
import sys

def verify_all(limit=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_path = os.path.join(os.path.dirname(script_dir), 'catalog', 'catalog.json')
    
    with open(catalog_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    print(f"Total items in catalog: {len(items)}")
    if limit:
        items = items[:limit]
        print(f"Checking first {limit} items...")
        
    ok_count = 0
    fail_count = 0
    
    for idx, item in enumerate(items, 1):
        url = item.get('stream_url')
        title = item.get('title')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) PublicDomainCatalogValidator/1.0',
            'Range': 'bytes=0-100'
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                code = resp.status
                ct = resp.headers.get('Content-Type', '')
                print(f"[{idx}/{len(items)}] [OK {code}] {title[:40]} ({ct})")
                ok_count += 1
        except Exception as e:
            print(f"[{idx}/{len(items)}] [FAIL] {title[:40]} -> {e}")
            fail_count += 1
            
    print(f"\nVerification Results: {ok_count} OK, {fail_count} Failed out of {len(items)} items checked.")

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    verify_all(limit)
