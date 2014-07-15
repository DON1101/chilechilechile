#!/bin/bash
VIRTUAL_ENV=$1
shift

. ${VIRTUAL_ENV}/bin/activate

cd ${VIRTUAL_ENV}/src/

python manage.py $@
