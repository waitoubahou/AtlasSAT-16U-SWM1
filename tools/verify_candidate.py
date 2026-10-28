"""Check the portable public subset; no private-workspace lookup or network access."""
from pathlib import Path
import argparse, ast, hashlib, json, re
from urllib.parse import unquote
ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.venv', '__pycache__', 'working', 'analysis_runs'}
STUDY = ROOT / 'studies/2A-orbital-analysis'

def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not SKIP.intersection(p.relative_to(ROOT).parts))

def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            digest.update(block)
    return digest.hexdigest()

def check(pdf_links=False, verify_manifest=True):
    findings = []; link_records = []; paths = files()
    personal = re.compile(r'(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/](?![\\/])(?:Users|Documents and Settings)[\\/]|/(?:home|Users)/[A-Za-z0-9_.-]+/)')
    contact = re.compile(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9_.-]+\.[A-Za-z]{2,}')
    secrets = re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}')
    # Exactly the professional contact present in the author-approved publication sources.
    one = next((STUDY/'documents').glob('*OnePager*.tex'))
    approved = set(contact.findall(one.read_text(encoding='utf-8')))
    if len(approved) != 1:
        findings.append('Expected one author-approved publication contact')
    if (ROOT/'.git').exists():
        findings.append('Unexpected Git metadata')
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in {'.zip','.tif','.tiff','.gpkg','.bpc','.bsp','.tls','.tpc','.log','.pfb','.pyc'}:
            findings.append(rel+': excluded payload type')
        if path.suffix.lower() in {'.pdf','.png'}:
            continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except UnicodeDecodeError:
            findings.append(rel+': unexpected binary'); continue
        if personal.search(text): findings.append(rel+': personal absolute path')
        addresses=set(contact.findall(text))
        if addresses-approved: findings.append(rel+': unapproved contact address')
        if addresses and path.suffix != '.tex': findings.append(rel+': contact outside approved publication source')
        if secrets.search(text): findings.append(rel+': possible credential')
        if path.suffix == '.py':
            try: ast.parse(text)
            except SyntaxError: findings.append(rel+': Python syntax error')
        targets=[]
        if path.suffix=='.md':
            targets += re.findall(r'\]\(([^)]+)\)',text)
            targets += re.findall(r'<(?:img|a)\s+[^>]*?(?:src|href)="([^"]+)"',text)
        if path.suffix=='.tex':
            targets += re.findall(r'\\href\{([^}]+)\}',text)
            targets += re.findall(r'\\(?:includegraphics)(?:\[[^]]*\])?\{([^}]+)\}',text)
            targets += re.findall(r'\\input\{([^}]+)\}',text)
        for target in targets:
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target) or target.startswith('#'): continue
            target=unquote(target.split('#')[0]).strip('<>')
            local=(path.parent/target).resolve()
            if not local.exists() and path.suffix=='.tex':
                groups=re.findall(r'\\graphicspath\{((?:\{[^}]+\})+)\}',text)
                for group in groups:
                    for prefix in re.findall(r'\{([^}]+)\}',group):
                        alternative=(path.parent/prefix/target).resolve()
                        if alternative.is_file(): local=alternative; break
            okay=local.is_relative_to(ROOT) and local.exists()
            link_records.append(dict(file=rel,target=target,exists=okay,kind='source'))
            if not okay: findings.append(rel+': unresolved local target '+target)
    if pdf_links:
        from pypdf import PdfReader
        for path in paths:
            if path.suffix!='.pdf': continue
            reader=PdfReader(path)
            data=str(reader.metadata)
            for page_no,page in enumerate(reader.pages,1):
                data += page.extract_text() or ''
                for item in page.get('/Annots',[]):
                    action=item.get_object().get('/A')
                    if not action: continue
                    action=action.get_object()
                    target=action.get('/URI',action.get('/F'))
                    if not target: continue
                    if hasattr(target,'get'): target=target.get('/UF',target.get('/F',''))
                    target=str(target)
                    if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target) or target.startswith('#'):continue
                    local=(path.parent/unquote(target.split('#')[0])).resolve()
                    okay=local.is_relative_to(ROOT) and local.exists()
                    link_records.append(dict(file=path.relative_to(ROOT).as_posix(),page=page_no,target=target,exists=okay,kind='pdf'))
                    if not okay: findings.append(path.name+': unresolved PDF target '+target)
            if personal.search(data):findings.append(path.name+': personal absolute path in PDF')
            if secrets.search(data):findings.append(path.name+': possible credential in PDF')
            if set(contact.findall(data))-approved:findings.append(path.name+': unapproved PDF contact')
    manifest=ROOT/'MANIFEST.sha256'
    if manifest.exists() and verify_manifest:
        expected={}
        for line in manifest.read_text().splitlines():
            digest,rel=line.split('  ',1); expected[rel]=digest
            if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest: findings.append('Manifest mismatch: '+rel)
        if {p.relative_to(ROOT).as_posix() for p in paths}-{'MANIFEST.sha256'} != expected.keys():
            findings.append('Unlisted or missing manifest files')
    return dict(passed=not findings,files_checked=len(paths),local_links_checked=len(link_records),pdf_links_checked=sum(x['kind']=='pdf' for x in link_records),links=link_records,findings=findings,scope='Bounded static privacy/link/integrity heuristics; no security or legal certification')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf-links',action='store_true',help='Also inspect all PDF actions/text; requires pypdf')
    args=parser.parse_args(); result=check(args.pdf_links)
    print(json.dumps(result,indent=2));raise SystemExit(not result['passed'])
