#!/usr/bin/env bash
uvicorn apps.gateway.app.main:app --reload --port 8000
