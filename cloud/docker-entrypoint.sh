#!/bin/sh

exec poetry run uvicorn cloud.main:app --host 0.0.0.0
