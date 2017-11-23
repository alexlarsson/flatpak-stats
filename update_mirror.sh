#!/bin/bash

REPO=https://flathub.org/repo/

if ! test -f flathub.gpg; then
    wget https://flathub.org/repo/flathub.gpg
fi
ostree --repo=mirror init
ostree --repo=mirror remote add --no-gpg-verify origin $REPO || true
ostree --repo=mirror pull --mirror --commit-metadata-only --depth=-1 origin

#for ref in `ostree --repo=mirror refs`; do ostree --repo=mirror log $ref --raw | awk "{ if (\$1 ==\"commit\") { print \$2 \" $ref\" ; }}"; done | sort
#ostree show --repo=mirror --print-metadata-key=xa.ref f28c4305ddbbd09c8cd001e704dbcb67d59005eedde3d68770bd2495ca92a8d8
