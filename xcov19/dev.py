"""
Runs the application for local development. This file should not be used to start the
application for production.

Refer to https://www.uvicorn.org/deployment/ for production deployments.
"""

import os
import importlib
import importlib.util as importlib_util

try:
    if importlib_util.find_spec("uvicorn", package="sys.modules"):
        importlib.import_module("uvicorn")
except ModuleNotFoundError:
    print("uvicorn not installed. Trying hypercorn")

from rich.console import Console

try:
    import uvloop
except ModuleNotFoundError:
    pass
else:
    uvloop.install()

from app.main import app


if __name__ == "__main__":
    os.environ["APP_ENV"] = "dev"
    port = int(os.environ.get("APP_PORT", 44777))

    console = Console()
    console.rule("[bold yellow]Running for local development", align="left")
    console.print(f"[bold yellow]Visit http://localhost:{port}/docs")

    if importlib_util.find_spec("hypercorn", package="sys.modules"):
        import asyncio
        from hypercorn.config import Config
        from hypercorn.asyncio import serve

        config = Config()

        config.bind = [f"localhost:{port}"]
        config.debug = True
        config.use_reloader = True

        asyncio.run(serve(app, config))
