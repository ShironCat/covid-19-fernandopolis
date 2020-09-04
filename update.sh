#!/bin/sh

cd chart-generator
pipenv run gen
cd ..
git add -A
git commit -m "atualização $(date)"
git push
