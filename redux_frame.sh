#!/bin/bash
n=$1; p=$(printf %04d $n)
mkdir -p assets/gr/$p
replicate run black-forest-labs/flux-redux-dev --input redux_image=@assets/gf/$p.png --input aspect_ratio=4:5 --output assets/gr/$p >/dev/null 2>&1
