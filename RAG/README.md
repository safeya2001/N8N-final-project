## ⚽ Caster Sport - Policy‑Aware Customer Support (RAG API)

### High‑Level Flow

1. **Policies ingestion**: the server loads all `.txt` policy files from the `policies/` folder and builds a FAISS vector index using sentence embeddings.
2. **Incoming request**: an external system sends a `POST /ask` request with either `question` or `emailBody` (plus optional metadata like `emailFrom`, `emailSubject`, `chatId`). 
3. **Retrieval step**: the server retrieves the most relevant policy chunks for the given question using the vector index (RAG).
4. **LLM generation**: context + question are sent to OpenRouter (Gemini model) to generate a well‑structured email (subject + body).
5. **Structured response**: the API returns JSON containing the suggested `emailSubject`, the final `answer` (email body), and any IDs/metadata echoed back.

---

This project is a Retrieval-Augmented Generation (RAG) system for **Caster Sport** customer support.  
It reads policy text files (`.txt`), builds a vector knowledge base (Embeddings + FAISS), and exposes a **Flask HTTP API** that returns:

- **A suggested email subject** tailored to the customer query.
- **A ready‑to‑send email body**, written in a professional style and in the user’s language (Arabic or English).

The API can be consumed by any external system, for example:

- Email management systems.
- CRMs or agent dashboards.
- Any web/chat/backend integration that can call HTTP endpoints.



---

## 1. Project Structure (inside `RAG`)

- **`rag_server.py`**: Flask server that loads policies, builds embeddings, and exposes the API.
- **`policies/`**: Folder containing plain‑text policy documents used by the RAG system.
- **`.env.example`**: Example environment configuration containing `OPENROUTER_API_KEY`.
- **`run.bat`** (Windows): Convenience script to install dependencies and run the server.
- **`README.md`**: This documentation file.

Default content of the `policies/` folder:

| File | Topic |
|------|-------|
| `returns_refunds.txt` | Returns and refunds policy |
| `shipping_delays.txt` | Shipping delays policy |
| `damaged_goods.txt` | Damaged items policy |
| `password_account.txt` | Password/account management policy |
| `general_contact.txt` | General contact / support policy |
| `cancel_shipment.txt` | Shipment cancellation policy |
| `exchange_policy.txt` | Exchange policy |

You can freely edit these files or add new `.txt` files with any name.

---

## 2. Prerequisites

- **Operating System**: Windows 10 or later.
- **Python**: Recommended Python ≥ 3.9.
- **Internet connection**: Required to call the OpenRouter API.

Check Python installation:

```bash
py --version
```

If this fails, install Python and ensure it is added to your `PATH`.

---

## 3. Environment and API Keys

1. Navigate to the project folder:

   ```bash
   cd "Final project\RAG"
   ```

2. Create a `.env` file from the example:

   - Option 1: From File Explorer, copy `.env.example` and rename the copy to `.env`.
   - Option 2: From a terminal (PowerShell/CMD):

     ```bash
     copy .env.example .env
     ```

3. Open `.env` and set your **valid OpenRouter API key**:

   ```env
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

   - **Important**: Do not commit this key to Git or share it publicly.

---

## 4. Running the Server (Windows)

### Recommended: use `run.bat`

1. Go to the `RAG` folder.
2. **Double‑click** `run.bat`.
3. The script will:
   - Install or update the required Python packages:
     - `flask`
     - `langchain-core`
     - `langchain-community`
     - `langchain-openai`
     - `langchain-huggingface`
     - `langchain-text-splitters`
     - `faiss-cpu`
     - `sentence-transformers`
     - `python-dotenv`
   - Start the server:

     ```bash
     py rag_server.py
     ```

4. In the terminal, you should see logs similar to:

   - `Loading RAG (policies + embeddings)...`
   - `RAG ready.`
   - `Starting server on port 5050...`

5. By default, the server listens on:

   - `http://localhost:5050`

Verify that the server is running by opening a browser and visiting:

```text
http://localhost:5050/health
```

Expected response:

```json
{"status": "ok"}
```

---

## 5. Architecture Overview

### 5.1 Policy Retriever

On first request (or at startup), `rag_server.py`:

1. Scans all `.txt` files in the `policies/` folder.
2. Splits them into smaller text chunks using:
   - `RecursiveCharacterTextSplitter` with chunk size 800 and overlap 100.
3. Computes embeddings for all chunks using:
   - `sentence-transformers/all-MiniLM-L6-v2`.
4. Builds a FAISS vector store and exposes it as a LangChain retriever, returning the top‑`k` relevant chunks per query.

If the `policies/` directory is missing or contains no valid documents, the system will respond with the error code `no_policies`.

### 5.2 Answer Generation (LLM via OpenRouter)

When a question is received, the server:

1. Uses the retriever to fetch the most relevant policy chunks.
2. Sends both the context and the question to `ChatOpenAI` (via OpenRouter) with the model:

   - `google/gemini-2.0-flash-001`

3. The system prompt instructs the model to:
   - Produce a **single‑line email subject** on the first line.
   - Add a blank line.
   - Then generate a **well‑structured, professional email body** (greeting, content, closing) in the user’s language.
4. The helper `_parse_email_response` splits the raw model output into `subject` and `body` and normalizes them for the API response.

---

## 6. Available API Endpoints

### 6.1 Health Check

- **Endpoint**: `GET /health`  
- **Response**:

```json
{
  "status": "ok"
}
```

### 6.2 Ask Policy‑Aware Question

- **Endpoint**: `POST /ask`  
- **Content-Type**: `application/json`

#### Request Body

At least one of the following fields must be provided (to define the question):

- **`question`**: Free‑form question text.
- **`emailBody`**: Raw customer email body you want to answer.

Optional context fields (echoed back in the response):

- **`emailFrom` / `email_from`**: Customer email address.
- **`emailSubject` / `email_subject`**: Original email subject, if any.
- **`chatId` / `chat_id`**: Conversation identifier in your own system.

Example request:

```http
POST /ask
Content-Type: application/json

{
  "question": "Hi, I would like to know your return policy.",
  "emailFrom": "customer@example.com",
  "emailSubject": "Return policy inquiry",
  "chatId": "thread-123"
}
```

#### Response Body

Successful response example:

```json
{
  "answer": "Full email body ready to send...",
  "error": "",
  "emailFrom": "customer@example.com",
  "emailSubject": "Re: Return policy inquiry",
  "chatId": "thread-123"
}
```

- **`answer`**: Final email body text, ready to send to the customer.
- **`emailSubject`**:
  - If you provided an original subject in the request, it will be returned as `Re: <original subject>` (unless already starting with `Re:`).
  - If no subject was provided, a model‑generated subject is used.
- **`error`**:
  - Empty string `""` on success.
  - Or an error code, for example:
    - `"no_question"`: No question content was provided.
    - `"no_policies"`: No policy documents were found or loaded.

Error response example (HTTP 400: missing question):

```json
{
  "answer": "",
  "error": "no_question",
  "emailFrom": "",
  "emailSubject": "Chat",
  "chatId": ""
}
```

---

## 7. Editing and Adding Policies

1. Open the `policies/` folder.
2. Edit any existing file (for example, `returns_refunds.txt`) with the real Caster Sport policy text.
3. Optionally, add new policy files, e.g.:

   - `loyalty_points.txt` for a loyalty points policy.

4. **Restart** the server (`run.bat` or `py rag_server.py`) so that:
   - Embeddings are rebuilt.
   - The new/updated policies are loaded into the vector store.

Any time you modify policy text files, a server restart is required.

---

## 8. Example Usage from PowerShell / CMD

After starting the server on `localhost:5050`, you can test it with `curl` (CMD):

```bash
curl -X POST http://localhost:5050/ask ^
  -H "Content-Type: application/json" ^
  -d "{ \"question\": \"What is your refund policy?\" }"
```

From **PowerShell**:

```powershell
$body = @{
  question     = "I want to know your shipping delay policy."
  emailFrom    = "customer@example.com"
  emailSubject = "Shipping delay"
  chatId       = "order-987"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5050/ask" -Body $body -ContentType "application/json"
```

You can adapt these examples to integrate with your own backend or tooling.

---

## 9. Troubleshooting

- **Issue**: Response contains `error: "no_policies"`  
  - **Check**:
    - `policies/` exists inside the `RAG` folder.
    - It contains at least one non‑empty `.txt` file.
    - You restarted the server after adding or editing policy files.

- **Issue**: Authentication / OpenRouter errors  
  - **Check**:
    - `OPENROUTER_API_KEY` in `.env` is correct and active.
    - The machine has a working internet connection.

- **Issue**: `py` command not found or Python not recognized  
  - **Check**:
    - Python is installed and added to the system `PATH`.
    - If `py` does not work, try using `python` instead in the scripts/commands.

---

## 10. Final Notes

- This project is intended as a **core policy‑aware customer support engine** based on manually authored policy documents.
- The HTTP API is intentionally simple so it can be integrated easily with email handlers, CRMs, or web backends via a single `POST /ask` call.
- Whenever you introduce major changes (new policies, different model, new endpoints, etc.), you should update this `README.md` to keep it in sync with the implementation.
