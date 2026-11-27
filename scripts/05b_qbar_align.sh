#!/usr/bin/env bash
# Document how to pass ADMIXTURE Q files to the qbar repository.
# Untested here (qbar is not installed in this environment).
# Repo: https://github.com/Xuzhen-Li/qbar

set -Ceu
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "--dry-run" ] || [ $# -eq 0 ]; then
  printf '%s\n' "usage: 05b_qbar_align.sh QGLOB OUTPREFIX"
  printf '%s\n' "Install and run qbar from https://github.com/Xuzhen-Li/qbar"
  printf '%s\n' "qbar sorts ADMIXTURE Q files, aligns columns across K, and plots structure barplots."
  if [ "${1:-}" = "--dry-run" ]; then
    exit 2
  fi
  exit 0
fi
printf '%s\n' "qbar is not invoked automatically in this wrapper; see --help."
exit 3
