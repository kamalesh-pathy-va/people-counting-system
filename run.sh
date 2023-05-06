#!/bin/bash
cd /home/kamaleshpathy/Downloads/final_test/
git pull origin main
python3 /home/kamaleshpathy/Downloads/final_test/server/serve.py &
python3 /home/kamaleshpathy/Downloads/final_test/main.py

