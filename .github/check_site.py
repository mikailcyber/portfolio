from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, shutil

root=Path(__file__).resolve().parents[1]
files=list(root.glob('*.html'))+list(root.glob('*.css'))+[root/'script.js',root/'.nojekyll']+[p for p in (root/'assets').rglob('*') if p.is_file() and not any(s.startswith('.') for s in p.relative_to(root/'assets').parts)]
errors=[]
references=[]
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if key in ('href','src','poster') and value:references.append((current,value))
for current in root.glob('*.html'):
    parser=Links();parser.feed(current.read_text(encoding='utf-8-sig'))
for current in root.glob('*.css'):
    references.extend((current,m[1]) for m in re.findall(r"url\(\s*([\"']?)(.*?)\1\s*\)",current.read_text(encoding='utf-8-sig')))
checked=0
for source,url in references:
    parsed=urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:continue
    if parsed.path.startswith('/'):
        errors.append(f'{source.name}: root-absolute path {url}');continue
    target=(source.parent/unquote(parsed.path)).resolve()
    if not target.is_relative_to(root) or not target.exists():errors.append(f'{source.name}: missing {url}')
    checked+=1
if errors:raise SystemExit('\n'.join(errors))
out=root/'dist';out.mkdir(exist_ok=True)
for source in files:
    relative=source.relative_to(root)
    target=out/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
assert not (out/'.wrangler').exists()
assert not (out/'.github').exists()
print(f'{checked} local references checked; {len(files)} website files prepared in dist/.')
