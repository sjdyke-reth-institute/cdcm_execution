#!/bin/zsh
# Shell script running tests for CDCM
#
# Author:
#   R Murali Krishnan
#
# Date:
#   05.09.2023
#

pytest .

trash *.h5
trash *.html
