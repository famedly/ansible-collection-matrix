#!/usr/bin/env bash
cd ../../
while read -r line; do
    find plugins -name "*.py" ! -path "plugins/module_utils/*" | xargs -I {} -n 1 printf "{} $line\n"
done <"tests/sanity/ignore.template"
