#!/usr/bin/env bash
cd ../../
while read -r line; do
    find plugins/modules -name "*.py" | xargs -I {} -n 1 printf "{} $line\n"
done <"tests/sanity/ignore.template"
