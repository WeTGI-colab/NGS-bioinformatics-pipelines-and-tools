#!/usr/bin/env python3
"""Auto-update tool versions in index.html from each repo's latest release/tag.

Reads tools.json, queries the GitHub API for the latest release (or newest tag)
of each repo, and rewrites the version text in index.html WITHOUT changing layout.

Env:
  TOOLS_TOKEN  GitHub token with read access to the (private) tool repos.
  DRYRUN=1     Use a fake tag "TEST" instead of calling the API (for local testing).
"""
import json, os, re, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
CFG  = os.path.join(ROOT, "tools.json")
TOKEN = os.environ.get("TOOLS_TOKEN", "")
DRY = os.environ.get("DRYRUN") == "1"


def _api(url):
    hdr = {"Accept": "application/vnd.github+json", "User-Agent": "diagram-version-bot"}
    if TOKEN:
        hdr["Authorization"] = f"Bearer {TOKEN}"
    return urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30)


def latest_version(repo):
    """Return the latest release tag_name, or the newest tag by semver."""
    if DRY:
        return "TEST"
    try:
        r = _api(f"https://api.github.com/repos/{repo}/releases/latest")
        tag = json.load(r).get("tag_name")
        if tag:
            return tag
    except urllib.error.HTTPError as e:
        if e.code not in (404,):
            print(f"WARN  {repo}: releases/latest -> HTTP {e.code}")
    except Exception as e:
        print(f"WARN  {repo}: releases/latest -> {e}")
    # fallback: newest tag by numeric sort
    try:
        r = _api(f"https://api.github.com/repos/{repo}/tags?per_page=100")
        tags = [t["name"] for t in json.load(r)]
        if tags:
            return sorted(tags, key=lambda t: [int(x) for x in re.findall(r"\d+", t)] or [0])[-1]
    except Exception as e:
        print(f"WARN  {repo}: tags -> {e}")
    return None


def main():
    html = open(HTML, encoding="utf-8").read()
    cfg = json.load(open(CFG))
    updated = 0
    for t in cfg["tools"]:
        name, repo = t["name"], t["repo"]
        where, suffix = t.get("where", "pname"), t.get("suffix", "")
        ver = latest_version(repo)
        if not ver:
            print(f"SKIP  {name} ({repo}) — no release/tag found")
            continue
        if where == "pname":
            pat = re.compile(r'(<span class="txt">' + re.escape(name) +
                             r'</span><span class="pver">)([^<]*)(</span>)')
            html, n = pat.subn(lambda m: m.group(1) + ver + suffix + m.group(3), html)
        else:  # header (tab title)
            pat = re.compile(r'(' + re.escape(name) + r' )v?[0-9][^ ]*( —)')
            html, n = pat.subn(lambda m: m.group(1) + ver + m.group(2), html)
        if n == 0:
            print(f"WARN  {name}: pattern matched 0 times (check the name in index.html)")
        else:
            print(f"OK    {name} -> {ver}{suffix}  ({n}x)")
            updated += 1
    open(HTML, "w", encoding="utf-8").write(html)
    print(f"Done. {updated} tools updated.")


if __name__ == "__main__":
    main()
