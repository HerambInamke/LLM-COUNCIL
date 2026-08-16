# LLM Council Architecture & Data Flow

## Project Overview
LLM Council is a 3-stage deliberation system where multiple LLMs collaboratively answer user questions. It consists of a React/Vite frontend and a FastAPI backend that communicates with the OpenRouter API.

## Directory Structure

### `/backend` (FastAPI)
The backend acts as the orchestrator for the LLM council.
- **`main.py`**: The FastAPI entry point. Sets up CORS, defines the API routes (`/api/conversations`), and handles Server-Sent Events (SSE) for streaming the multi-stage progress back to the frontend.
- **`council.py`**: The core business logic. It handles the 3 distinct stages:
  1. `stage1_collect_responses`: Queries all council models in parallel.
  2. `stage2_collect_rankings`: Anonymizes Stage 1 responses and asks each model to rank them.
  3. `stage3_synthesize_final`: Passes the original query, all responses, and all peer rankings to the Chairman model to generate the final synthesized answer.
- **`openrouter.py`**: Handles the HTTP communication with the OpenRouter API. Contains `query_model()` and `query_models_parallel()` for efficient asynchronous API calls.
- **`config.py`**: Loads environment variables from `.env`. Configures the `COUNCIL_MODELS` and the `CHAIRMAN_MODEL`.
- **`storage.py`**: Manages local persistence. Saves conversation histories as JSON files in the `/data/conversations/` directory.

### `/frontend` (React + Vite)
The frontend provides a ChatGPT-like interface that visually breaks down the 3 stages.
- **`src/App.jsx`**: The main orchestration component. Manages state for the conversation list, the active conversation, and the progressive loading indicators.
- **`src/api.js`**: Client for interacting with the backend. Handles standard REST calls and parses the Server-Sent Events (SSE) stream for real-time UI updates.
- **`src/components/ChatInterface.jsx`**: The main chat window. Renders user messages and conditionally renders the Stage 1, Stage 2, and Stage 3 components based on the SSE events.
- **`src/components/Stage1.jsx`**: Displays individual model responses in a tabbed view using `react-markdown`.
- **`src/components/Stage2.jsx`**: Displays the raw evaluations and the aggregated rankings. De-anonymizes the models client-side for the user while keeping them anonymous for the API logic.
- **`src/components/Stage3.jsx`**: Displays the final synthesized answer from the Chairman model. Includes a "Copy" button.
- **`src/components/Sidebar.jsx`**: Manages conversation history navigation.

### `/data/conversations/`
- Local JSON storage where chat histories are saved. Excluded from git via `.gitignore`.

### Root Configuration
- **`.env` / `.env.example`**: Securely stores the `OPENROUTER_API_KEY` and allows overriding default models.
- **`start.sh`**: Helper script to boot both the FastAPI backend (port 8001) and Vite frontend (port 5173) simultaneously.
- **`pyproject.toml`**: Python dependency and project metadata file (uses `uv` and `hatchling`).

## Data Flow (End-to-End)

1. **User Input**: User types a query in `ChatInterface.jsx` and hits Send.
2. **Frontend Request**: `api.js` sends a POST request to `/api/conversations/{id}/message/stream`.
3. **Backend Orchestration (`council.py`)**:
   - Yields `stage1_start` event to frontend.
   - Fetches individual responses in parallel via `openrouter.py`.
   - Yields `stage1_complete` event.
   - Yields `stage2_start` event.
   - Anonymizes responses and prompts models to rank each other.
   - Yields `stage2_complete` event with extracted rankings and metadata.
   - Yields `stage3_start` event.
   - Sends everything to the Chairman model.
   - Yields `stage3_complete` event.
4. **Storage**: `storage.py` saves the completed conversation to disk as JSON.
5. **UI Update**: `ChatInterface.jsx` progressively updates the UI as each Server-Sent Event arrives, updating the bouncing dots loaders and rendering the Markdown outputs.
