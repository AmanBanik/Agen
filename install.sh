#!/bin/bash
echo "Installing Agen V2..."
# Create a virtual environment if you want, but for global CLI we typically just use pipx or pip
pip install -e .
echo "Installation complete! Run 'agen' to start."
