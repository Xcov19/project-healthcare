#!/bin/bash

echo "listing all files";
ls;
if [ -f "xcov19.db" ]; then 
    echo "removing database";
    rm xcov19.db; 
fi;

APP_ENV=dev APP_DB_ENGINE_URL="sqlite+aiosqlite:///xcov19.db" poetry run python3 -m xcov19.dev