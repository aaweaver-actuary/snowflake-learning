#!/usr/bin/env zsh

FOLDER=/home/andy/code/snowflake/

SERIES=(
    GDP
    GDPC1
    GDPDEF
    UNRATE

    # Auto Loan Rates
    TERMCBAUTO48NS
    RIFLPBCIANM60NM
    RIFLPBCIANM72NM

)

python3 ${FOLDER}/fred.py get GDP
python3 ${FOLDER}/fred.py get GDPDEF

