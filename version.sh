#!/bin/bash
# Generates a version string from config.py
MAJOR=$(sed -n 's/.*VERSION = (\([[:digit:]]\+\), [[:digit:]]\+, [[:digit:]]\+).*/\1/p' config.py)
MINOR=$(sed -n 's/.*VERSION = ([[:digit:]]\+, \([[:digit:]]\+\), [[:digit:]]\+).*/\1/p' config.py)
REVISION=$(sed -n 's/.*VERSION = ([[:digit:]]\+, [[:digit:]]\+, \([[:digit:]]\+\)).*/\1/p' config.py)

VERSION="$MAJOR.$MINOR.$REVISION"

# Write this Verison to the Dockerfile
sed -i -e "s/LABEL Version=\"[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\"/LABEL Version=\"$VERSION\"/" docker/Dockerfile.prod
sed -i -e "s/LABEL Version=\"[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\"/LABEL Version=\"$VERSION\"/" docker/Dockerfile.arm64v8.prod
sed -i -e "s/LABEL Version=\"[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\"/LABEL Version=\"$VERSION\"/" docker/Dockerfile.dev
sed -i -e "s/LABEL Version=\"[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\"/LABEL Version=\"$VERSION\"/" docker/Dockerfile.arm64v8.dev

# This will return the Version for the makefile to tag the image
echo $VERSION
