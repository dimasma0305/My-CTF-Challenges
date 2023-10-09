#!/bin/sh
SECRET_KEY=TEST uvicorn main:app --workers 24
