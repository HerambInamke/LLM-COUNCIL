# LLM Council

The idea of this repo is that instead of asking a question to a single LLM provider, you can consult your own "LLM Council". This is a local web app that looks like ChatGPT, except it uses OpenRouter to send your query to multiple LLMs in parallel. It then asks them to review and rank each other's work, and finally, a Chairman LLM synthesizes everything into one polished final response.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all LLMs individually, and the responses are collected. The individual responses are shown in a "tab view", so you can inspect them all one by one.
2. **Stage 2: Peer Review**. Each LLM is given the responses of the other LLMs. Under the hood, the LLM identities are anonymized (Response A, Response B, etc.) so that models can't play favorites when judging their outputs. Each LLM is asked to rank the others based on accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman of the LLM Council takes all of the models' responses and peer rankings and compiles them into a single final, well-reasoned answer that is presented to you.

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for Python project management and `npm` for the frontend.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure Environment

Create a `.env` file in the project root by copying the example file:

```bash
cp .env.example .env
```

Edit your new `.env` file to include your OpenRouter API key:
```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

Get your API key at [openrouter.ai](https://openrouter.ai/). 

### 3. Customize Your Council (Optional)

By default, the council uses 100% free models from OpenRouter to ensure everyone can run this out of the box without hitting payment walls:

**Default Council Members:**
- `dots-studio/dots-3-note-preview:free`
- `nvidia/nemotron-3.5-lightning:free`
- `poolside/laguna-s-2.1:free`

**Default Chairman:**
- `liquid/lfm-2.5-2.6b:free`

You can easily customize these models by either adding `COUNCIL_MODELS` and `CHAIRMAN_MODEL` to your `.env` file (as shown in `.env.example`), or editing `backend/config.py` directly. For best results, we recommend using powerful models like `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`, and `google/gemini-1.5-pro` if you have API credits!

## Running the Application

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Run manually**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Tech Stack

- **Backend:** FastAPI (Python), async httpx, OpenRouter API
- **Frontend:** React + Vite, react-markdown
- **Storage:** Local JSON files in `data/conversations/`
- **Package Management:** `uv` for Python, `npm` for JavaScript
