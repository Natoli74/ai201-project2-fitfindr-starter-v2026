# Running FitFindr

## Runtime

- **Required Python:** 3.11, 3.12, or 3.13. Python 3.14 and newer are
  rejected by `test.py`.
- **Verified local virtual environment:** Python 3.13.7 (`.venv`).
- No `pyproject.toml`, `Pipfile`, Poetry lockfile, or uv lockfile is present.

## Dependencies

Install the requirements from the repository root. The project uses bounded
version ranges rather than exact package versions:

```text
python-dotenv>=1.0,<1.2
google-genai>=1.0,<2.0
mcp>=1.0,<2.0
flask>=3.0,<4.0
gunicorn>=21.2,<24.0
```

`google-genai` is the remote model client. `mcp` provides the retrieval
service connection. Flask and Gunicorn are only needed for the HTTP service
entry point.

## Model and vector data

There are **no local model-weight files** and **no vector index** in this
checkout:

- Model weights: 0 bytes stored locally; generation uses the configured
  Gemini API model (`AI201_MODEL`, default `gemini-3.6-flash-lite`).
- Vector index: 0 bytes; retrieval reads the local JSON listing data through
  the MCP server and does not use embeddings or a vector database.
- `data/listings.json`: approximately 20 KB on disk.
- `data/wardrobe_schema.json`: approximately 4 KB on disk.
- The checked-in `.venv` is approximately 74 MB, including installed
  dependencies; it contains no model weights.

No model download or index-build step is required. Create `.env` from
`.env.example` and set `GEMINI_API_KEY` before running a model-backed query.
`AI201_MODEL` may be set there to override the default model name.

## Clean-checkout setup

From the cloned `unit-3-4` directory:

### macOS / Linux

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY.
python test.py
```

### Windows PowerShell

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY.
python test.py
```

## Exact execution command

With the virtual environment activated and `GEMINI_API_KEY` configured, the
clean terminal command for the project is:

```bash
python app.py ask 'vintage graphic tee under $30'
```

`app.py` is the main command-line entry point. Other available entry points
include:

```bash
python app.py fields
python app.py listings --full -n 6
python app.py examples
python agent.py
python mcp_client.py
python run_eval.py --label before
python measure_runtime.py
python serve.py
```

For the HTTP service, use `gunicorn serve:app` after installing the listed
dependencies.

`measure_runtime.py` runs ten representative queries, appends one structured
JSON line per execution to `runtime.log`, and updates the instrumentation and
cost sections in `README.md`.
