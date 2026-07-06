import re
import urllib.request
import urllib.error

with open('README.md', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Replace all occurrences of azurestaticapps URLs with the new one
text = re.sub(r'https?://[a-zA-Z0-9\-\.]+\.azurestaticapps\.net[^\s\]\)"\']*', 
              'https://polite-hill-08013890f.7.azurestaticapps.net/iam/sign-in', text)

# Replace all occurrences of github.io URLs for the landing page
text = re.sub(r'https?://[a-zA-Z0-9\-\.]+\.github\.io/saferoute-website/?', 
              'https://upc-pre-202610-1asi0729-11896-fivetech.github.io/saferoute-website/', text)

# Replace all occurrences of azurewebsites.net URLs for backend
text = re.sub(r'https?://[a-zA-Z0-9\-\.]+\.azurewebsites\.net[^\s\]\)"\']*', 
              'https://saferoute-os.azurewebsites.net/swagger-ui/index.html', text)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced URLs in README.md")

# Now check for broken URLs
urls = re.findall(r'https?://[^\s)\]\"\'<>]+', text)
urls = set(urls)
urls = [u for u in urls if not u.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')) and 'localhost' not in u]

print(f'Checking {len(urls)} URLs...')
broken = []
for u in urls:
    if "upcedupe-my.sharepoint.com" in u:
        continue # Skip sharepoint videos
    if "drive.google.com" in u or "1drv.ms" in u:
        continue # Skip google drive and one drive videos as they are private
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as e:
        if e.code not in [403, 401]:
            broken.append((u, str(e)))
    except Exception as e:
        broken.append((u, str(e)))

print('---BROKEN URLS---')
for u, err in broken:
    print(f'{u} - {err}')
print('DONE')
