#!/bin/bash

echo "Activating Poetry environment..."
source $(poetry env info --path)/bin/activate

echo "Running Griffith College Chatbot..."
python main.py
