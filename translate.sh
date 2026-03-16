#!/usr/bin/env bash

set -e

PROJECT="Piggyzilla"
VERSION="1.0"
AUTHOR="Miauware"
EMAIL="miauware@outlook.com"
YEAR=$(date +%Y)

pybabel extract \
  -F babel.cfg \
  -o messages.pot \
  --project="$PROJECT" \
  --version="$VERSION" \
  --msgid-bugs-address="$EMAIL" \
  --copyright-holder="$PROJECT" \
  .

# INFO: change pot header
sed -i "s/# FIRST AUTHOR <EMAIL@ADDRESS>, .*/# $AUTHOR <$EMAIL>, $YEAR./" messages.pot

pybabel update -i messages.pot -d translations

# INFO: change po headers
find translations -name "messages.po" | while read -r file; do
  sed -i "s/# FIRST AUTHOR <EMAIL@ADDRESS>, .*/# $AUTHOR <$EMAIL>, $YEAR./" "$file"
  sed -i "s/Last-Translator:.*/Last-Translator: $AUTHOR <$EMAIL>\\\\n/" "$file"
done

pybabel compile -d translations