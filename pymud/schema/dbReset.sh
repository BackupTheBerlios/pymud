#! /bin/bash
dropdb mud
sleep 1
createdb mud
sleep 1
psql mud < mud.sql
psql mud < muddata.sql
