"""Launcher for the standalone preview. Puts backend/ on sys.path."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "knit360_core"))

import uvicorn

if __name__ == "__main__":
	uvicorn.run("knit360_core.standalone.app:app", host="127.0.0.1", port=8321, reload=False)
