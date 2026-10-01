import json, re, sys

# Builds the release notes from the changelog shown in the About screen
version = sys.argv[1]
code = ''.join(version.split('.'))
code = code.zfill(3)
number = int(code)

# English texts
lang = {}
for line in open('texts/en_US.lang', encoding='utf-8'):
    if '=' in line and not line.startswith('#'):
        k, v = line.rstrip('\n').split('=', 1)
        lang[k.strip()] = v.split('\t#')[0].strip()


# Removes minecraft color codes
def clean(text):
    return re.sub('§.', '', text).strip()


# About screen sections, ignoring full line comments
raw = open('ui/zk_ui/about/about_screen.json', encoding='utf-8').read()
raw = '\n'.join(l for l in raw.split('\n') if not l.strip().startswith('//'))
sections = json.loads(raw)
section = sections.get(f'changelog{code}_section@zk_about_common.main_sections')
if not section:
    sys.exit(0)

headings = {
    'new_features_title': 'New features',
    'changes_title': 'Changes',
    'fixes_title': 'Fixes',
}

out = []
title = lang.get(f'zk.about.changelog{code}.title')
if title:
    out.append(f'## {clean(title).capitalize()}')
for control in section['controls']:
    key = next(iter(control))
    name = key.split('@')[0]
    if name in headings:
        out += ['', f'### {headings[name]}']
    elif name.startswith('label_'):
        text = lang.get(f'zk.about.changelog{number}.label{control[key]["$line"]}')
        if text:
            out.append(text)
print('\n'.join(out))
