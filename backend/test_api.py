import httpx, json

data = json.load(open('test_request.json', encoding='utf-8'))
resp = httpx.post('http://127.0.0.1:8000/api/recommend/generate', json=data, timeout=30)
result = resp.json()

print(f"Status: {resp.status_code}")

rush = result.get("rush", [])
stable = result.get("stable", [])
safe = result.get("safe", [])
summary = result.get("summary", {})

print(f"Rush: {len(rush)}")
print(f"Stable: {len(stable)}")
print(f"Safe: {len(safe)}")
print(f"Summary: {summary}")

for tier_name, tier_list in [("Rush", rush), ("Stable", stable), ("Safe", safe)]:
    if tier_list:
        u = tier_list[0]
        print(f"\n{tier_name}[0]: {u['university_name']}")
        print(f"  Rank match: {u['rank_match_score']}, Subject adapt: {u['subject_adapt_score']}, Total: {u['total_score']}")
        print(f"  Tags: {u['tags']}")
        for m in u.get("recommended_majors", [])[:2]:
            print(f"  Major: {m['major_name']} (adapt={m['subject_adapt_score']})")
            print(f"    Adapt tags: {m['adapt_tags']}")
            print(f"    Risk notes: {m['risk_notes']}")
