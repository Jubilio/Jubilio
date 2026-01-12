import requests
import os
from collections import Counter

USER = "Jubilio"
headers = {"Accept": "application/vnd.github.v3+json"}
token = os.getenv("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"token {token}"

def fetch_all_repos(user):
    url = f"https://api.github.com/users/{user}/repos?per_page=100"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Error fetching repos: {resp.status_code} {resp.text}")
        return []
    return resp.json()

def fetch_langs(repo):
    resp = requests.get(repo["languages_url"], headers=headers)
    if resp.status_code != 200:
        print(f"Error fetching langs for {repo.get('name')}: {resp.status_code}")
        return {}
    return resp.json()

def main():
    repos = fetch_all_repos(USER)
    counter = Counter()
    for repo in repos:
        langs = fetch_langs(repo)
        # Ensure values are integers (skip error responses that might look like dicts)
        if isinstance(langs, dict) and all(isinstance(v, int) for v in langs.values()):
            counter.update(langs)

    # Gera Markdown de lista ordenada por bytes
    total = sum(counter.values())
    total = sum(counter.values())
    lines = ["| Language | % of code |", "| --- | --- |"]
    for lang, size in counter.most_common():
        pct = size / total * 100
        if pct < 0.1: continue
        lines.append(f"| {lang} | {pct:.1f}% |")

    md = "\n".join(lines)
    # Insere no README
    with open("README.md", "r+", encoding="utf-8") as f:
        content = f.read()
        before, _, rest = content.partition("<!-- START_LANGUAGES -->")
        _, _, after = rest.partition("<!-- END_LANGUAGES -->")
        new = before + "<!-- START_LANGUAGES -->\n" + md + "\n<!-- END_LANGUAGES -->" + after
        f.seek(0)
        f.truncate()
        f.write(new)

if __name__ == "__main__":
    main()

