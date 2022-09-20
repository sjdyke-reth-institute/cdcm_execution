# This script makes and publishes the lecture book
# taken from : 
#   https://github.com/PredictiveScienceLab/data-analytics-se/blob/master/make.sh

# Make it
jupyter-book build docs --all

# Publish it
ghp-import -n -p -f docs/_build/html