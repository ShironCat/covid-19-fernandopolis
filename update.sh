#!/bin/sh

cd chart-generator
pipenv install
pipenv run gen
cd ..
read -n 1 -s -r -p "Press any key to continue"
git add -A
git commit -m "atualização $(date)"
git push
