"""Utilitats compartides: càrrega i normalització de data/people.json."""
import json, re, unicodedata, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "people.json"
ROLES = ["director", "senior-member", "postdoc", "phd-student", "master-student",
         "research-assistant", "visiting", "collaborator"]
STATUS = ["current", "former"]
LINK_KEYS = ["scholar", "dblp", "orcid", "github", "linkedin", "semanticscholar", "openalex"]

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))["people"]

def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def norm_url(u):
    if not u: return None
    u = re.sub(r"^https?://(www\.)?", "", u.strip().lower()).split("#")[0]
    base, _, q = u.partition("?")
    m = re.search(r"(?:^|&)(?:user|id)=([^&]+)", q)   # p. ex. Google Scholar: la identitat és a ?user=
    return base.rstrip("/") + (f"?user={m.group(1)}" if m else "")
