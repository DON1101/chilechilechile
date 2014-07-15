#!/bin/bash
VIRTUAL_ENV=$1
PROJECT_APP=chilechilechile
shift

. ${VIRTUAL_ENV}/bin/activate

lock=${VIRTUAL_ENV}/lock.manage.${1}

cd ${VIRTUAL_ENV}/src/${PROJECT_APP}

nice with-lock-ex -w $lock python manage.py $@
