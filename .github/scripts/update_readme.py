#!/usr/bin/env python3
"""Recompute the live stats in README.md. Run by .github/workflows/stats.yml."""
import os, re, json, urllib.request, urllib.parse

USER = "abhishek-gola"
TOKEN = os.environ["GITHUB_TOKEN"]

def get(url, auth=True):
    h = {"Accept": "application/vnd.github+json", "User-Agent": USER}
    if auth:
        h["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
        return r.read().decode("utf-8", "replace")

def count(q):
    q = urllib.parse.quote(q)
    return json.loads(get(f"https://api.github.com/search/issues?q={q}&per_page=1"))["total_count"]

RAW = "https://raw.githubusercontent.com/opencv/opencv/5.x/modules/dnn/test/"
total = len(re.findall(r'^\s*\{"test_', get(RAW + "test_onnx_conformance.cpp", auth=False), re.M))
deny  = len(re.findall(r'^"test_', get(RAW + "test_onnx_conformance_layer_parser_denylist.inl.hpp", auth=False), re.M))
rate  = (total - deny) / total * 100

merged   = count(f"author:{USER} org:opencv type:pr is:merged")
reviewed = count(f"reviewed-by:{USER} org:opencv type:pr")

stats = (f"So far that's **{merged} merged pull requests** across the OpenCV "
         f"organisation and **{reviewed}** more reviewed.")
onnx  = (f"OpenCV currently passes **{rate:.0f}%** of the {total}-test ONNX "
         f"conformance suite ({total - deny} of {total}),")

src = open("README.md", encoding="utf-8").read()
for tag, body in (("STATS", stats), ("ONNX", onnx)):
    src = re.sub(rf"(<!--{tag}:start-->).*?(<!--{tag}:end-->)",
                 lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", src, flags=re.S)
open("README.md", "w", encoding="utf-8").write(src)
print(f"merged={merged} reviewed={reviewed} onnx={rate:.1f}% ({total-deny}/{total})")
