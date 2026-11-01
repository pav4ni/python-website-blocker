"""Read/write blocked domains in the system hosts file (needs admin/root)."""
import os
import platform
import shutil
from urllib.parse import urlparse

START = "# >>> website-blocker start >>>"
END = "# <<< website-blocker end <<<"
REDIRECT_IP = "127.0.0.1"


def hosts_path() -> str:
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    return "/etc/hosts"


def normalize(site: str) -> str:
    """'https://www.Example.com/page' -> 'example.com'"""
    site = site.strip().lower()
    if "//" not in site:
        site = "//" + site
    host = urlparse(site).netloc or site
    host = host.split(":")[0]
    return host[4:] if host.startswith("www.") else host


def _split(lines):
    """Return (before, managed_domains, after) around our marker block."""
    if START in lines and END in lines:
        s, e = lines.index(START), lines.index(END)
        domains = []
        for line in lines[s + 1:e]:
            parts = line.split()
            if len(parts) >= 2 and not parts[1].startswith("www."):
                domains.append(parts[1])
        return lines[:s], domains, lines[e + 1:]
    return lines, [], []


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def get_blocked(path: str = None):
    path = path or hosts_path()
    return sorted(_split(_read(path))[1])


def set_blocked(domains, path: str = None):
    path = path or hosts_path()
    if not os.path.exists(path + ".bak"):
        shutil.copy(path, path + ".bak")  # one-time backup
    before, _, after = _split(_read(path))
    block = []
    if domains:
        block.append(START)
        for d in sorted(set(domains)):
            block.append(f"{REDIRECT_IP} {d}")
            block.append(f"{REDIRECT_IP} www.{d}")
        block.append(END)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(before + block + after) + "\n")


def block(sites, path: str = None):
    current = set(get_blocked(path))
    current.update(normalize(s) for s in sites if s.strip())
    set_blocked(current, path)
    return sorted(current)


def unblock(sites, path: str = None):
    remove = {normalize(s) for s in sites}
    remaining = [d for d in get_blocked(path) if d not in remove]
    set_blocked(remaining, path)
    return remaining
