"""
Multi-thread alice-bot conversation fetcher.
Fetches all exchanges between 0coceo and alice-bot across all threads.
"""
import subprocess, json, re
from collections import Counter

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
ALICE_DID = "did:plc:rb7crpqhlukud3m4fojg2eie"
OUTPUT_PATH = "/home/agent/company/docs/alice-archaeology-data.json"

STOPWORDS = {
    'the','a','an','and','or','but','in','on','at','to','for','of','with','by',
    'from','is','it','its','this','that','we','our','i','you','be','are','was',
    'were','have','has','had','do','does','did','not','as','if','so','what','how',
    'when','where','who','which','there','their','they','them','then','than','into',
    'can','will','just','about','up','out','like','more','also','even','still',
    'only','no','one','two','three','all','each','any','some','new','same','other',
    'both','your','my','me','us','he','she','his','her','way','every','after',
    'before','through','between','while','because','without','within','over',
    'under','again','been','very','much','most','own','these','those','here',
    'now','back','get','got','could','would','should','might','make','take',
    'see','come','go','say','know','think','feel','need','want','keep','find','give',
    'something','nothing','anything','everything','part','point'
}

def bsky(method, params):
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", method, json.dumps(params)],
        capture_output=True, text=True
    )
    if r.returncode != 0: return None
    try: return json.loads(r.stdout)
    except: return None

def get_author_posts(did, limit=200):
    posts = []
    cursor = None
    while len(posts) < limit:
        params = {"actor": did, "limit": min(100, limit - len(posts))}
        if cursor: params["cursor"] = cursor
        data = bsky("app.bsky.feed.getAuthorFeed", params)
        if not data: break
        feed = data.get("feed", [])
        if not feed: break
        for item in feed:
            post = item.get("post", {})
            record = post.get("record", {})
            reply = record.get("reply", {})
            posts.append({
                "uri": post.get("uri"),
                "cid": post.get("cid"),
                "author_did": post.get("author", {}).get("did"),
                "author": post.get("author", {}).get("handle"),
                "text": record.get("text", ""),
                "created_at": record.get("createdAt", ""),
                "likes": post.get("likeCount", 0),
                "parent_uri": reply.get("parent", {}).get("uri") if reply else None,
                "root_uri": reply.get("root", {}).get("uri") if reply else None,
            })
        cursor = data.get("cursor")
        if not cursor: break
    return posts

def get_words(text):
    return [w.lower() for w in re.findall(r"[a-z']+", text.lower()) 
            if len(w) > 3 and w.lower() not in STOPWORDS]

def run():
    print("Fetching posts...")
    our_posts = get_author_posts(OUR_DID, 200)
    alice_posts = get_author_posts(ALICE_DID, 200)
    
    by_uri = {}
    for p in our_posts + alice_posts:
        by_uri[p["uri"]] = p
    
    # Find all direct reply exchanges
    seen = set()
    pairs = []
    for p in our_posts + alice_posts:
        if p["parent_uri"] and p["parent_uri"] in by_uri and p["uri"] not in seen:
            parent = by_uri[p["parent_uri"]]
            other_did = ALICE_DID if p["author_did"] == OUR_DID else OUR_DID
            if parent["author_did"] == other_did:
                seen.add(p["uri"])
                pairs.append(p)
    
    pairs.sort(key=lambda p: p["created_at"])
    
    # Vocabulary over time
    our_words = Counter()
    alice_words = Counter()
    our_by_time = []
    alice_by_time = []
    shared_over_time = []
    
    for i, p in enumerate(pairs):
        words = get_words(p["text"])
        if p["author_did"] == OUR_DID:
            our_words.update(words)
            our_by_time.append(p["created_at"])
        else:
            alice_words.update(words)
            alice_by_time.append(p["created_at"])
        
        if (i + 1) % 10 == 0 or i == len(pairs) - 1:
            shared = set(our_words.keys()) & set(alice_words.keys())
            shared_over_time.append({
                "exchange_num": i + 1,
                "shared_count": len(shared),
                "timestamp": p["created_at"]
            })
    
    shared = set(our_words.keys()) & set(alice_words.keys())
    shared_list = sorted(shared, key=lambda w: our_words[w] + alice_words[w], reverse=True)
    
    # Top 20 terms
    top_terms = [[w, our_words[w] + alice_words[w]] for w in shared_list[:20]]
    
    # Build exchanges list
    exchanges = [
        {
            "num": i + 1,
            "author": p["author"],
            "text": p["text"],
            "created": p["created_at"][:16],
            "likes": p["likes"],
            "uri": p["uri"],
        }
        for i, p in enumerate(pairs)
    ]
    
    output = {
        "total_exchanges": len(pairs),
        "shared_vocab": sorted(list(shared)),
        "top_terms": top_terms,
        "shared_over_time": shared_over_time,
        "word_emergence": {},
        "exchanges": exchanges,
        "generated_at": "2026-03-11"
    }
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Exchanges: {len(pairs)}")
    print(f"Shared vocab: {len(shared)}")
    print(f"Top terms: {[t[0] for t in top_terms[:10]]}")
    print(f"Written to {OUTPUT_PATH}")

if __name__ == "__main__":
    run()
