#!/bin/bash

REPO=http://flathub.org/repo/

ostree --repo=mirror init
ostree --repo=mirror remote add --no-gpg-verify origin $REPO || true
ostree --repo=mirror pull --mirror --commit-metadata-only --depth=-1 origin

for ref in `ostree --repo=mirror refs`; do ostree --repo=mirror log $ref --raw | awk "{ if (\$1 ==\"commit\") { print \$2 \" $ref\" ; }}"; done | sort
