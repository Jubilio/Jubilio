import requests
from collections import Counter

USER = "Jubilio"
headers = {"Accept": "application/vnd.github.v3+json"}

def fetch_all_repos(user):
    url = f"https://api.github.com/users/{user}/repos?per_page=100"
    return requests.get(url, headers=headers).json()

def fetch_langs(repo):
    return requests.get(repo["languages_url"], headers=headers).json()

def main():
    repos = fetch_all_repos(USER)
    counter = Counter()
    for repo in repos:
        langs = fetch_langs(repo)
        counter.update(langs)

    # Gera Markdown de lista ordenada por bytes
    total = sum(counter.values())
    lines = ["| Linguagem | % do código |", "|---|---|"]
    for lang, size in counter.most_common():
        pct = size / total * 100
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

