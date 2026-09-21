#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$repo_root"
build_dir="$repo_root/_build"

# Keep TeX Live caches inside the repository workspace. This avoids writes to
# the user home directory and gives LuaTeX a writable cache location.
export TEXMFVAR="$repo_root/.texlive-var"
export TEXMFCONFIG="$repo_root/.texlive-config"
latexmk_args="-f -g"

mkdir -p .texlive-var .texlive-config
mkdir -p "$build_dir"

have_diff_source=true
old_source_label="HEAD:main.tex"
old_source_ref="HEAD:main.tex"

if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  have_diff_source=false
elif ! git ls-files --error-unmatch -- main.tex >/dev/null 2>&1; then
  have_diff_source=false
elif ! git diff --cached --quiet -- main.tex; then
  old_source_label="staged main.tex"
  old_source_ref=":main.tex"
fi

tmp_old=""
if [ "$have_diff_source" = true ]; then
  tmp_old="$(mktemp)"
fi

trap 'rm -f "$tmp_old"' EXIT

rm -f "$build_dir/main.pdf" "$build_dir/main-d.pdf" "$build_dir/main-d.tex"
rm -f "$repo_root/main-d.tex"
export BUILD_DIFF=0
unset LATEXDIFF_OLD_SOURCE LATEXDIFF_NEW_SOURCE

if [ "$have_diff_source" = true ]; then
  git show "$old_source_ref" > "$tmp_old"
fi

# shellcheck disable=SC2086
latexmk $latexmk_args -outdir="$build_dir" main.tex
cp "$build_dir/main.pdf" "$repo_root/main.pdf"

if [ "$have_diff_source" = true ]; then
  export BUILD_DIFF=1
  export LATEXDIFF_OLD_SOURCE="$tmp_old"
  export LATEXDIFF_NEW_SOURCE="main.tex"
  # shellcheck disable=SC2086
  latexmk $latexmk_args -jobname=main-d -outdir="$build_dir" main.tex
  cp "$build_dir/main-d.pdf" "$repo_root/main-d.pdf"
fi

printf 'Built working-copy PDF: %s/main.pdf\n' "$repo_root"
printf 'Build directory: %s\n' "$build_dir"
if [ "$have_diff_source" = true ]; then
  printf 'Built comparison PDF: %s/main-d.pdf\n' "$repo_root"
  printf 'Reference version: %s\n' "$old_source_label"
else
  printf 'Comparison PDF skipped: no tracked Git reference for main.tex\n'
fi
