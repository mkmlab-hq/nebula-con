#!/usr/bin/env bash
set -euo pipefail

echo "== Git sanity =="
git fetch --all --prune
git status
echo

echo "== Detect unmerged/conflict markers =="
if git grep -nE '^(<<<<<<<|=======|>>>>>>>)' -- . ; then
  echo "Conflict markers found above. Fix them before merging."
  exit 1
fi
echo "No conflict markers found."
echo

echo "== Optional: simulate merge with origin/main (no commit) =="
if git rev-parse --verify origin/main >/dev/null 2>&1; then
  git merge --no-commit --no-ff origin/main || true
  if [ -n "$(git ls-files -u)" ]; then
    echo "Would conflict with origin/main:"
    git ls-files -u
    git merge --abort || true
    exit 1
  fi
  git merge --abort || true
else
  echo "origin/main not found; skipped."
fi
echo

echo "== Whitespace/EOL check =="
git diff --check || true
echo

if ls **/*.py >/dev/null 2>&1; then
  echo "== Python checks =="
  python3 -m compileall -q .
  if command -v ruff >/dev/null 2>&1; then ruff check . || true; fi
  if command -v black >/dev/null 2>&1; then black --check . || true; fi
  if command -v mypy >/dev/null 2>&1; then mypy . || true; fi
  echo
fi

if [ -f package.json ]; then
  echo "== Node checks =="
  npm run -s typecheck || true
  npm run -s build || true
  echo
fi

echo "== Large file scan (>10MB) =="
MAX=10485760
git ls-files -z | xargs -0 -I{} bash -lc 'f="{}"; s=$(wc -c < "$f" || echo 0); if [ "$s" -gt '"$MAX"' ]; then echo "$f is >10MB ($s bytes)"; fi' || true
echo
echo "Done." 