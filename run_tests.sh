#!/bin/bash
set -x
# pytest -vvv             pytests/
# pytest -vvv -s       -l pytests/
  pytest -vvv -s --pdb -l pytests/

