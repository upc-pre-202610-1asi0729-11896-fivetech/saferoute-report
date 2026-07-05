import re
import urllib.request
import urllib.error

with open('README.md', 'r', encoding='utf-8') as f:
    text = f.read()

urls = re.findall(r'https?://[^\s)\]\"\'<>]+', text)
urls = set(urls)

urls = [u for u in urls if not u.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')) and 'localhost' not in u]

print(f'Checking {len(urls)} URLs...')
broken = []
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as e:
        # 403 Forbidden is often a working URL but blocked by bot protection
        if e.code not in [403, 401]:
            broken.append((u, str(e)))
    except Exception as e:
        broken.append((u, str(e)))

print('---BROKEN URLS---')
for u, err in broken:
    print(f'{u} - {err}')
