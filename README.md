# Caster Sport – AI-Powered Customer Support System

> **Intelligent, Policy-Aware Customer Support Automation**
> Combining RAG (Retrieval-Augmented Generation), workflow automation, and vector databases to deliver instant, accurate, policy-compliant customer service responses.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue.svg)](https://supabase.com)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Database Setup](#2-database-setup)
  - [3. RAG API Setup](#3-rag-api-setup)
  - [4. n8n Workflow Setup](#4-n8n-workflow-setup)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Workflow Details](#workflow-details)
- [Usage Guide](#usage-guide)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**Caster Sport Customer Support System** is an end-to-end intelligent customer service platform designed specifically for e-commerce operations. The system automatically processes incoming customer emails, classifies inquiries, retrieves relevant information from both policy documents and order databases, and generates professional, context-aware email responses.

### What Makes This System Special?

- **Policy-Aware**: Uses RAG to ensure all responses align with company policies
- **Order-Intelligent**: Automatically retrieves and processes customer order information
- **Context-Sensitive**: Generates responses based on customer history and order status
- **Multi-Lingual**: Supports both English and Arabic responses
- **Fully Automated**: From email receipt to draft generation with minimal human intervention
- **Vector Search**: Utilizes pgvector for semantic search over policies and email history

---

## Key Features

### 🤖 Intelligent Email Classification
- Automatically categorizes emails into:
  - Order Inquiries
  - Cancellation Requests
  - Cancellation Confirmations
  - General Questions
- Intent detection using AI language models

### 📚 RAG-Powered Knowledge Base
- Retrieval-Augmented Generation for policy-compliant answers
- FAISS vector store for efficient similarity search
- Sentence transformers for semantic understanding
- Real-time policy document retrieval

### 🗄️ Smart Order Management
- PostgreSQL database with Supabase
- Real-time order status tracking
- Automatic order retrieval by customer email
- Support for complex order workflows (pending → shipped → delivered → cancelled)

### 📧 Automated Email Generation
- Professional, ready-to-send email drafts
- Context-aware subject lines
- Personalized greetings and closings
- Multi-language support (English/Arabic)

### 🔄 Workflow Automation with n8n
- Visual workflow builder
- Gmail integration for email triggers
- Conditional routing based on intent
- Error handling and fallback mechanisms

### 🔍 Vector Search Capabilities
- pgvector extension for PostgreSQL
- Cosine similarity search on email embeddings
- IVFFlat indexing for performance
- Semantic retrieval over history

---

## System Architecture

```
┌─────────────────┐
│  Gmail Inbox    │
│  (Customer)     │
└────────┬────────┘
         │
         │ Email Trigger
         ▼
┌─────────────────────────────────────────────┐
│           n8n Workflow Engine               │
│  ┌───────────────────────────────────────┐  │
│  │  1. Email Classification (AI Agent)   │  │
│  └───────────────┬───────────────────────┘  │
│                  │                           │
│  ┌───────────────▼───────────────────────┐  │
│  │  2. Intent Routing                    │  │
│  │     • Order Inquiry                   │  │
│  │     • Cancel Order                    │  │
│  │     • Confirm Cancel                  │  │
│  │     • General Question                │  │
│  └───┬───────────────────────────────┬───┘  │
│      │                               │      │
│      │ Order Tracks                  │ General
│      ▼                               ▼      │
│  ┌─────────────────┐        ┌────────────┐ │
│  │  Supabase DB    │        │  RAG API   │ │
│  │  Query Orders   │        │  /ask      │ │
│  └────────┬────────┘        └──────┬─────┘ │
│           │                        │        │
│           ▼                        ▼        │
│  ┌────────────────────────────────────────┐ │
│  │  AI Agent: Generate Email Response     │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
└───────────────────┼──────────────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │  Gmail Draft  │
            │  (Ready)      │
            └───────────────┘
```

### Architecture Components

#### 1. **Email Input Layer (Gmail)**
   - Monitors inbox for new customer emails
   - Extracts sender, subject, and body content
   - Triggers n8n workflow on new message

#### 2. **Orchestration Layer (n8n)**
   - **Classification Module**: Uses OpenRouter/Gemini AI to classify email intent
   - **Routing Engine**: Directs requests to appropriate handlers
   - **Data Retrieval**: Queries Supabase for order information
   - **Response Generation**: Coordinates with RAG API or direct AI agents

#### 3. **Knowledge Layer (RAG API)**
   - **Document Ingestion**: Loads policy text files from `/policies/`
   - **Embedding Generation**: Creates vector embeddings using sentence-transformers
   - **Vector Store**: FAISS index for fast similarity search
   - **LLM Integration**: OpenRouter with Gemini 2.0 Flash for response generation
   - **API Endpoints**:
     - `GET /health` - Health check
     - `POST /ask` - Process customer questions

#### 4. **Data Layer (Supabase/PostgreSQL)**
   - **Orders Table**: Customer order management with status tracking
   - **Emails Table**: Email content storage with vector embeddings
   - **pgvector Extension**: Native vector operations in PostgreSQL
   - **Indexes**: Optimized for email lookups and similarity search

#### 5. **Output Layer (Gmail Drafts)**
   - Auto-generated email drafts
   - Ready for human review or auto-send
   - Professional formatting with proper greetings/closings

---

## Technology Stack

### Backend & API
- **Python 3.9+**: Core programming language
- **Flask 2.0+**: RESTful API framework for RAG service
- **LangChain**: RAG orchestration and LLM integration
- **FAISS**: Facebook AI Similarity Search for vector operations
- **sentence-transformers**: Text embedding models

### Database & Storage
- **Supabase**: PostgreSQL-as-a-Service platform
- **PostgreSQL 14+**: Relational database
- **pgvector**: Vector similarity search extension
- **JSONB**: Semi-structured data storage (order items, metadata)

### AI & Machine Learning
- **OpenRouter API**: LLM gateway (Gemini 2.0 Flash)
- **Sentence Transformers**: `all-MiniLM-L6-v2` for embeddings
- **LangChain**: RAG framework and prompt engineering
- **Google Gemini 2.0 Flash**: Fast, cost-effective LLM

### Automation & Workflows
- **n8n**: Visual workflow automation platform
- **Gmail API**: Email integration (OAuth2)
- **Webhook Integration**: HTTP endpoints for inter-service communication

### Development Tools
- **python-dotenv**: Environment variable management
- **Git**: Version control
- **Markdown**: Documentation

---

## Prerequisites

### Software Requirements
- **Python**: 3.9 or higher ([Download](https://www.python.org/downloads/))
- **Git**: For cloning the repository ([Download](https://git-scm.com/))
- **n8n**: Self-hosted or cloud instance ([Documentation](https://docs.n8n.io/))
- **Gmail Account**: For email automation
- **Supabase Account**: Free tier available ([Sign up](https://supabase.com))

### API Keys & Credentials
- **OpenRouter API Key**: Get from [openrouter.ai](https://openrouter.ai/)
- **Gmail OAuth2 Credentials**: Configure in n8n
- **Supabase Project URL & API Key**: From Supabase dashboard

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: Minimum 4GB (8GB+ recommended for local embedding generation)
- **Storage**: ~500MB for dependencies and models
- **Network**: Stable internet connection for API calls

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/caster-sport-support.git
cd caster-sport-support
```

Or download the ZIP file and extract it.

---

### 2. Database Setup

#### 2.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the database to initialize (~2 minutes)
3. Navigate to **Project Settings → API**
4. Copy the following credentials:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **Anon/Public Key**: `eyJhbGc...` (long token)

#### 2.2 Enable pgvector Extension

1. In Supabase dashboard, go to **SQL Editor**
2. Create a new query and run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

3. Click **RUN** to execute

#### 2.3 Create Database Tables

Run the following SQL in the **SQL Editor**:

```sql
-- ==========================================
-- ORDERS TABLE
-- ==========================================
CREATE TABLE public.orders (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  order_number TEXT NOT NULL,
  customer_email TEXT NOT NULL,
  customer_name TEXT NULL,
  phone_number VARCHAR(20) NULL,
  status TEXT NULL DEFAULT 'pending',
  total_amount NUMERIC NULL,
  items JSONB NULL,
  created_at TIMESTAMPTZ NULL DEFAULT NOW(),
  CONSTRAINT orders_pkey PRIMARY KEY (id)
);

-- Indexes for performance
CREATE INDEX idx_orders_email ON public.orders(customer_email);
CREATE INDEX idx_orders_status ON public.orders(status);
CREATE INDEX idx_orders_number ON public.orders(order_number);

-- Add comments for documentation
COMMENT ON TABLE public.orders IS 'Customer orders with status tracking';
COMMENT ON COLUMN public.orders.status IS 'Values: pending, shipped, delivered, cancelled';

-- ==========================================
-- EMAILS TABLE (with vector embeddings)
-- ==========================================
CREATE TABLE public.emails (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  content TEXT NULL,
  embedding VECTOR NULL,
  metadata JSONB NULL,
  created_at TIMESTAMPTZ NULL DEFAULT NOW(),
  CONSTRAINT emails_pkey PRIMARY KEY (id)
);

-- Vector similarity index (IVFFlat)
CREATE INDEX IF NOT EXISTS emails_embedding_idx
  ON public.emails USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Index for timestamp queries
CREATE INDEX idx_emails_created ON public.emails(created_at DESC);

COMMENT ON TABLE public.emails IS 'Email content storage with vector embeddings for semantic search';
```

#### 2.4 Insert Sample Data (Optional)

```sql
-- Sample order
INSERT INTO public.orders (
  order_number,
  customer_email,
  customer_name,
  phone_number,
  status,
  total_amount,
  items
) VALUES (
  'CS-2024-001',
  'customer@example.com',
  'Ahmed Ali',
  '+962791234567',
  'pending',
  299.99,
  '[
    {
      "product": "Football Jersey",
      "size": "L",
      "quantity": 2,
      "price": 149.99
    }
  ]'::jsonb
);
```

#### 2.5 Verify Tables

Run this query to confirm tables were created:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE';
```

Expected output:
```
orders
emails
```

---

### 3. RAG API Setup

#### 3.1 Navigate to RAG Directory

```bash
cd RAG
```

#### 3.2 Install Python Dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

Or use the convenience script (Windows only):
```bash
run.bat
```

#### 3.3 Configure Environment Variables

1. Create `.env` file:

**Windows (CMD):**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:

```env
# OpenRouter API Key (required)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: Change server port (default: 5050)
PORT=5050

# Optional: Enable debug mode
FLASK_DEBUG=False
```

**Important**:
- Never commit `.env` to Git
- Keep your API keys secure
- Get your OpenRouter key from: [openrouter.ai](https://openrouter.ai/)

#### 3.4 Add Policy Documents

The `policies/` folder contains the following default policy files:

- `returns_refunds.txt` - Return and refund policy
- `shipping_delays.txt` - Shipping delay handling
- `damaged_goods.txt` - Damaged item procedures
- `password_account.txt` - Account management
- `general_contact.txt` - General support info
- `cancel_shipment.txt` - Cancellation procedures
- `exchange_policy.txt` - Exchange guidelines

**To customize:**
1. Edit existing `.txt` files with your actual policies
2. Add new policies by creating new `.txt` files
3. Restart the server to reload

#### 3.5 Start the RAG Server

**Windows:**
```bash
run.bat
```

Or manually:
```bash
python rag_server.py
```

**macOS/Linux:**
```bash
python3 rag_server.py
```

#### 3.6 Verify RAG API

Open your browser and visit:
```
http://localhost:5050/health
```

Expected response:
```json
{"status": "ok"}
```

Test the `/ask` endpoint:
```bash
curl -X POST http://localhost:5050/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is your return policy?",
    "emailFrom": "test@example.com"
  }'
```

---

### 4. n8n Workflow Setup

#### 4.1 Install n8n

**Option 1: npm (recommended for development)**
```bash
npm install -g n8n
n8n start
```

**Option 2: Docker**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Access n8n at: `http://localhost:5678`

#### 4.2 Configure Credentials

1. **Gmail OAuth2**:
   - Go to **Credentials** → **New**
   - Select **Gmail OAuth2**
   - Follow Google OAuth setup wizard
   - Grant permissions for Gmail read/send

2. **OpenRouter API**:
   - Add new **HTTP Header Auth** credential
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_OPENROUTER_API_KEY`

3. **Supabase**:
   - Add **Supabase** credential
   - Host: Your project URL (e.g., `xxxxx.supabase.co`)
   - Service Role Key: Your anon/public API key

#### 4.3 Import Workflow

1. In n8n, click **Workflows** → **Import from File**
2. Select `N8N/Main Simple - V4 (1).json`
3. The workflow will load with all nodes

#### 4.4 Configure Workflow Nodes

Update the following nodes with your settings:

**RAG API Node:**
- URL: `http://localhost:5050/ask` (or your ngrok URL if remote)

**Supabase Nodes:**
- Select your Supabase credential
- Verify table names match (`orders`, `emails`)

**Gmail Nodes:**
- Select your Gmail OAuth2 credential
- Configure trigger filters if needed

#### 4.5 Activate Workflow

1. Click **Save** in the top-right
2. Toggle **Active** switch to ON
3. The workflow will now process incoming emails automatically

---

## Database Schema

### Orders Table

**Purpose**: Store and manage customer orders with lifecycle tracking.

| Column           | Type         | Constraints       | Description                              |
|------------------|--------------|-------------------|------------------------------------------|
| `id`             | UUID         | PRIMARY KEY       | Unique order identifier (auto-generated) |
| `order_number`   | TEXT         | NOT NULL          | Human-readable order number (e.g., CS-2024-001) |
| `customer_email` | TEXT         | NOT NULL          | Customer email address                   |
| `customer_name`  | TEXT         |                   | Customer full name                       |
| `phone_number`   | VARCHAR(20)  |                   | Customer phone number                    |
| `status`         | TEXT         | DEFAULT 'pending' | Order status (see values below)          |
| `total_amount`   | NUMERIC      |                   | Order total in currency units            |
| `items`          | JSONB        |                   | Array of order line items (JSON)         |
| `created_at`     | TIMESTAMPTZ  | DEFAULT NOW()     | Order creation timestamp                 |

**Status Values**:
- `pending`: Order placed, can be cancelled
- `shipped`: Order dispatched, cannot be cancelled (customer can refuse delivery)
- `delivered`: Order received by customer
- `cancelled`: Order cancelled

**Indexes**:
```sql
idx_orders_email   -- B-tree on customer_email
idx_orders_status  -- B-tree on status
idx_orders_number  -- B-tree on order_number
```

**Example Row**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "order_number": "CS-2024-001",
  "customer_email": "ahmed@example.com",
  "customer_name": "Ahmed Ali",
  "phone_number": "+962791234567",
  "status": "pending",
  "total_amount": 299.99,
  "items": [
    {
      "product": "Football Jersey",
      "size": "L",
      "quantity": 2,
      "price": 149.99
    }
  ],
  "created_at": "2024-12-15T10:30:00Z"
}
```

---

### Emails Table

**Purpose**: Store email content with vector embeddings for semantic search.

| Column      | Type        | Constraints | Description                                  |
|-------------|-------------|-------------|----------------------------------------------|
| `id`        | UUID        | PRIMARY KEY | Unique row identifier (auto-generated)       |
| `content`   | TEXT        |             | Full email text or policy content            |
| `embedding` | VECTOR      |             | Vector embedding (384-dimensional float array) |
| `metadata`  | JSONB       |             | Additional data (subject, sender, tags)      |
| `created_at`| TIMESTAMPTZ | DEFAULT NOW() | Record creation timestamp                  |

**Indexes**:
```sql
emails_embedding_idx  -- IVFFlat index on embedding (vector_cosine_ops)
idx_emails_created    -- B-tree on created_at DESC
```

**Vector Index Details**:
- **Type**: IVFFlat (Inverted File with Flat Compression)
- **Distance Metric**: Cosine similarity
- **Lists Parameter**: 100 (for ~10,000 vectors; adjust based on dataset size)
- **Embedding Dimension**: 384 (from `all-MiniLM-L6-v2` model)

**Example Row**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "content": "Dear customer, regarding your inquiry about our return policy...",
  "embedding": [0.123, -0.456, 0.789, ...], // 384 dimensions
  "metadata": {
    "subject": "Re: Return Policy Question",
    "sender": "support@castersport.com",
    "category": "policy",
    "language": "en"
  },
  "created_at": "2024-12-15T11:00:00Z"
}
```

---

### Database Usage by Workflow

| Table    | Intent Track       | Operation            | Query Example                                    |
|----------|--------------------|----------------------|--------------------------------------------------|
| `orders` | Order Inquiry      | `SELECT` (getAll)    | `WHERE customer_email = $1`                      |
| `orders` | Cancel Order       | `SELECT` (getAll)    | `WHERE customer_email = $1 AND status = 'pending'` |
| `orders` | Confirm Cancel     | `SELECT` + `UPDATE`  | `UPDATE ... SET status = 'cancelled' WHERE id = $1` |
| `emails` | Semantic Search    | Vector similarity    | `ORDER BY embedding <=> $1 LIMIT 5`              |

---

## API Documentation

### RAG API Endpoints

Base URL: `http://localhost:5050`

#### 1. Health Check

**Endpoint**: `GET /health`

**Response**: 200 OK
```json
{
  "status": "ok"
}
```

---

#### 2. Ask Question (RAG)

**Endpoint**: `POST /ask`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "question": "What is your return policy?",          // Required (or emailBody)
  "emailBody": "I want to return my order...",        // Alternative to question
  "emailFrom": "customer@example.com",                // Optional
  "emailSubject": "Return inquiry",                   // Optional
  "chatId": "thread-123"                              // Optional
}
```

**Parameters**:
- `question` (string, optional*): Free-form customer question
- `emailBody` (string, optional*): Full email body content
- `emailFrom` (string, optional): Customer email address
- `emailSubject` (string, optional): Original email subject
- `chatId` (string, optional): Conversation/thread identifier

*At least one of `question` or `emailBody` is required.

**Success Response**: 200 OK
```json
{
  "answer": "Dear Customer,\n\nThank you for contacting Caster Sport...",
  "emailSubject": "Re: Return inquiry",
  "emailFrom": "customer@example.com",
  "chatId": "thread-123",
  "error": ""
}
```

**Error Response**: 400 Bad Request
```json
{
  "answer": "",
  "emailSubject": "Chat",
  "emailFrom": "",
  "chatId": "",
  "error": "no_question"  // or "no_policies"
}
```

**Error Codes**:
- `no_question`: No question or emailBody provided
- `no_policies`: Policy documents not found or failed to load

**Example cURL**:
```bash
curl -X POST http://localhost:5050/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can I cancel my order after it has shipped?",
    "emailFrom": "customer@example.com",
    "emailSubject": "Order cancellation"
  }'
```

**Example Python**:
```python
import requests

response = requests.post(
    "http://localhost:5050/ask",
    json={
        "question": "What is your exchange policy?",
        "emailFrom": "customer@example.com"
    }
)

data = response.json()
print(data["answer"])
```

---

## Project Structure

```
Final project/
│
├── RAG/                              # Python RAG API Service
│   ├── rag_server.py                 # Flask server (main API)
│   ├── requirements.txt              # Python dependencies
│   ├── run.bat                       # Windows startup script
│   ├── .env.example                  # Environment template
│   ├── .env                          # Actual config (DO NOT COMMIT)
│   │
│   ├── policies/                     # Policy text files (RAG corpus)
│   │   ├── returns_refunds.txt
│   │   ├── shipping_delays.txt
│   │   ├── damaged_goods.txt
│   │   ├── password_account.txt
│   │   ├── general_contact.txt
│   │   ├── cancel_shipment.txt
│   │   └── exchange_policy.txt
│   │
│   └── README.md                     # RAG-specific documentation
│
├── N8N/                              # n8n Workflow Files
│   └── Main Simple - V4 (1).json     # Complete automation workflow
│
├── .gitignore                        # Git exclusions
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── README.md                         # This file (main documentation)
├── TECHNICAL REPORT.pdf              # Academic/technical report (PDF)
└── TECHNICAL REPORT.docx             # Academic/technical report (Word)
```

### Key Files Explained

**`rag_server.py`**:
- Core RAG API implementation
- Loads policies from `policies/` directory
- Creates FAISS vector index
- Exposes `/health` and `/ask` endpoints
- Integrates with OpenRouter/Gemini LLM

**`requirements.txt`**:
- Python package dependencies
- Flask, LangChain, FAISS, sentence-transformers
- Run `pip install -r requirements.txt`

**`run.bat`**:
- Windows convenience script
- Installs dependencies and starts server
- Double-click to run

**`.env.example`**:
- Template for environment variables
- Copy to `.env` and add your API keys

**`policies/`**:
- Plain text policy documents
- Each file represents one policy domain
- Automatically loaded and indexed by RAG system

**`Main Simple - V4 (1).json`**:
- n8n workflow definition
- Import into n8n to get the full automation

**`TECHNICAL REPORT.pdf`**:
- Comprehensive technical documentation
- Architecture diagrams
- Implementation details
- Use cases and testing

---

## Workflow Details

### n8n Workflow: Main Simple V4

#### Workflow Overview

The workflow implements a complete customer service automation pipeline with four distinct tracks:

1. **Order Inquiry Track**: Retrieve and display customer order information
2. **Cancel Order Track**: Process order cancellation requests
3. **Confirm Cancel Track**: Finalize order cancellations
4. **General Question Track**: Answer policy/general questions using RAG

#### Workflow Nodes Breakdown

**1. Gmail Trigger**
- **Type**: Trigger node
- **Function**: Monitors Gmail inbox for new emails
- **Filter**: Can be configured to filter by label, sender, subject, etc.
- **Output**: Email metadata (from, subject, body, attachments)

**2. AI Classifier Agent**
- **Type**: AI Agent node (OpenRouter)
- **Model**: Gemini 2.0 Flash
- **Function**: Classifies email intent into one of four categories
- **Prompt Engineering**:
  ```
  Classify this email into one category:
  - "Order Inquiry": Customer asking about order status
  - "Cancel Order": Customer wants to cancel
  - "Confirm Cancel": Follow-up to confirm cancellation
  - "General Question": Policy or general inquiry

  Email: {emailBody}

  Respond with only the category name.
  ```

**3. Switch Node (Intent Router)**
- **Type**: Routing node
- **Function**: Routes to correct track based on classification
- **Conditions**:
  - Route 0: `intent === "Order Inquiry"`
  - Route 1: `intent === "Cancel Order"`
  - Route 2: `intent === "Confirm Cancel"`
  - Route 3: `intent === "General Question"`

**4. Supabase Query Nodes** (Routes 0-2)
- **Type**: Database node
- **Operation**: `getAll` (SELECT)
- **Table**: `orders`
- **Filters**:
  - Order Inquiry: `customer_email = {{ $node["Gmail Trigger"].json["from"] }}`
  - Cancel Order: `customer_email = ... AND status = 'pending'`
  - Confirm Cancel: `customer_email = ... AND order_number = {{ extracted_number }}`

**5. RAG API Call** (Route 3)
- **Type**: HTTP Request node
- **Method**: POST
- **URL**: `http://localhost:5050/ask`
- **Body**:
  ```json
  {
    "question": "{{ $node["Gmail Trigger"].json["body"] }}",
    "emailFrom": "{{ $node["Gmail Trigger"].json["from"] }}",
    "emailSubject": "{{ $node["Gmail Trigger"].json["subject"] }}"
  }
  ```

**6. AI Response Generator Nodes**
- **Type**: AI Agent node
- **Function**: Generate contextual email response
- **Context Injection**:
  - Orders data from Supabase
  - Customer email/name
  - Original question
- **Output**: Professional email with greeting, content, closing

**7. Gmail Draft Creator**
- **Type**: Gmail node
- **Operation**: Create draft
- **To**: `{{ $node["Gmail Trigger"].json["from"] }}`
- **Subject**: `Re: {{ $node["Gmail Trigger"].json["subject"] }}`
- **Body**: `{{ $node["AI Response Generator"].json["answer"] }}`

#### Error Handling

- **Supabase Errors**: Fallback to generic "please contact support" message
- **RAG API Errors**: Retry mechanism with 3 attempts
- **Classification Errors**: Default to General Question track
- **LLM Errors**: Logged and escalated to human agent

---

## Usage Guide

### For End Users (Customers)

1. **Send an email** to your configured Gmail address
2. **Wait for processing** (typically 10-30 seconds)
3. **Receive a draft** in your Gmail drafts folder (or auto-sent if configured)

### For Customer Service Agents

1. **Monitor drafts**: Review auto-generated drafts before sending
2. **Edit if needed**: Modify tone, add personal touches, or clarify details
3. **Send**: Click send in Gmail when satisfied
4. **Track performance**: Monitor response quality and accuracy

### For Administrators

#### Adding New Policies

1. Navigate to `RAG/policies/`
2. Create a new `.txt` file (e.g., `warranty_policy.txt`)
3. Write the policy content in plain text
4. Restart the RAG server: `python rag_server.py`
5. Test with a question:
   ```bash
   curl -X POST http://localhost:5050/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is your warranty policy?"}'
   ```

#### Updating Existing Policies

1. Edit the `.txt` file in `RAG/policies/`
2. Save changes
3. Restart RAG server to reload
4. No database changes needed

#### Managing Orders

**Add order programmatically**:
```sql
INSERT INTO orders (order_number, customer_email, customer_name, status, total_amount, items)
VALUES (
  'CS-2024-123',
  'customer@example.com',
  'John Doe',
  'pending',
  150.00,
  '[{"product": "Running Shoes", "quantity": 1, "price": 150.00}]'::jsonb
);
```

**Update order status**:
```sql
UPDATE orders
SET status = 'shipped'
WHERE order_number = 'CS-2024-123';
```

**Query customer orders**:
```sql
SELECT * FROM orders
WHERE customer_email = 'customer@example.com'
ORDER BY created_at DESC;
```

#### Monitoring System Health

**Check RAG API**:
```bash
curl http://localhost:5050/health
```

**Check n8n workflow**:
- Go to n8n dashboard: `http://localhost:5678`
- View workflow executions
- Check for errors in execution logs

**Check database**:
```sql
-- Count orders by status
SELECT status, COUNT(*)
FROM orders
GROUP BY status;

-- Count emails with embeddings
SELECT COUNT(*)
FROM emails
WHERE embedding IS NOT NULL;
```

---

## Deployment

### Production Considerations

#### RAG API Deployment

**Option 1: Traditional Server (VPS/Dedicated)**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install gunicorn  # Production WSGI server
   ```

2. **Set environment variables**:
   ```bash
   export OPENROUTER_API_KEY=your_key_here
   export FLASK_ENV=production
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5050 rag_server:app
   ```

4. **Configure reverse proxy** (nginx):
   ```nginx
   server {
       listen 80;
       server_name api.castersport.com;

       location / {
           proxy_pass http://localhost:5050;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

**Option 2: Docker Deployment**

Create `Dockerfile` in `RAG/`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "rag_server:app"]
```

Build and run:
```bash
docker build -t caster-rag-api .
docker run -d -p 5050:5050 --env-file .env caster-rag-api
```

**Option 3: Cloud Platforms**

- **Google Cloud Run**: Serverless, auto-scaling
- **AWS Lambda + API Gateway**: Pay-per-request
- **Heroku**: Simple deployment with git push
- **Railway/Render**: Modern PaaS platforms

#### n8n Deployment

**Self-Hosted**:
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**n8n Cloud**: Managed hosting at [n8n.cloud](https://n8n.cloud)

#### Database (Supabase)

Already cloud-hosted! Production-ready features:
- Automatic backups
- Point-in-time recovery
- Connection pooling
- Global CDN
- 99.9% uptime SLA

#### Security Best Practices

1. **API Keys**:
   - Use environment variables, never hardcode
   - Rotate keys regularly
   - Use separate keys for dev/staging/production

2. **Database**:
   - Enable Row Level Security (RLS) in Supabase
   - Use service role key only on backend
   - Implement rate limiting

3. **HTTPS**:
   - Use SSL/TLS certificates (Let's Encrypt is free)
   - Force HTTPS redirects
   - Enable HSTS headers

4. **Network**:
   - Firewall rules to restrict access
   - VPN for administrative access
   - DDoS protection (Cloudflare)

5. **Monitoring**:
   - Set up logging (e.g., Sentry, LogRocket)
   - Monitor API usage and costs
   - Set up alerts for errors/downtime

---

## Troubleshooting

### Common Issues

#### RAG API Issues

**Issue**: `{"error": "no_policies"}`

**Solution**:
1. Verify `policies/` folder exists in `RAG/` directory
2. Check that it contains at least one `.txt` file with content
3. Restart the RAG server

---

**Issue**: OpenRouter API authentication error

**Solution**:
1. Verify `OPENROUTER_API_KEY` in `.env` is correct
2. Check key format: `sk-or-v1-...`
3. Confirm you have credits/quota on OpenRouter
4. Test key with:
   ```bash
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer $OPENROUTER_API_KEY"
   ```

---

**Issue**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
```bash
pip install -r requirements.txt
```

If still failing, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

#### n8n Workflow Issues

**Issue**: Gmail trigger not activating

**Solution**:
1. Re-authenticate Gmail OAuth2 in Credentials
2. Check Gmail API is enabled in Google Cloud Console
3. Verify trigger is set to "Active" mode
4. Check filter conditions aren't too restrictive

---

**Issue**: Supabase query returns no results

**Solution**:
1. Verify customer email exists in `orders` table
2. Check for case sensitivity: `customer_email` is case-sensitive
3. Confirm Supabase credential has correct URL and API key
4. Test query in Supabase SQL editor

---

**Issue**: RAG API call fails from n8n

**Solution**:
1. Verify RAG server is running: `curl http://localhost:5050/health`
2. If n8n is remote, use ngrok to expose RAG API:
   ```bash
   ngrok http 5050
   ```
   Update n8n HTTP node URL to ngrok URL
3. Check firewall rules allow connections

---

#### Database Issues

**Issue**: `pgvector` extension not available

**Solution**:
```sql
-- Enable in Supabase SQL editor
CREATE EXTENSION IF NOT EXISTS vector;
```

If error persists, contact Supabase support.

---

**Issue**: Slow vector similarity queries

**Solution**:
1. Ensure IVFFlat index exists:
   ```sql
   \d emails  -- In psql to see indexes
   ```
2. Rebuild index:
   ```sql
   DROP INDEX IF EXISTS emails_embedding_idx;
   CREATE INDEX emails_embedding_idx
     ON emails USING ivfflat (embedding vector_cosine_ops)
     WITH (lists = 100);
   ```
3. Adjust `lists` parameter based on data size:
   - 1K-10K rows: lists = 100
   - 10K-100K rows: lists = 1000
   - 100K+ rows: lists = sqrt(row_count)

---

**Issue**: JSONB query errors

**Solution**:
Use proper JSONB operators:
```sql
-- Check if key exists
SELECT * FROM orders WHERE items ? 'product';

-- Query nested values
SELECT * FROM orders WHERE items @> '[{"product": "Football Jersey"}]';
```

---

### Debugging Tips

1. **Enable verbose logging**:
   ```python
   # In rag_server.py
   app.config['DEBUG'] = True
   ```

2. **Check n8n execution logs**:
   - Click on workflow execution
   - View input/output of each node
   - Check error messages in red nodes

3. **Monitor database queries**:
   - Supabase Dashboard → Logs → Postgres Logs
   - Enable real-time query logging

4. **Test components in isolation**:
   - RAG API: Use cURL/Postman
   - Database: Run queries in SQL editor
   - n8n: Test workflow manually with sample data

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Start for Contributors

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with descriptive messages**:
   ```bash
   git commit -m "feat: add multi-language support for responses"
   ```
6. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Contribution Areas

- **Policy Templates**: Add industry-specific policy templates
- **Language Support**: Expand multi-language capabilities
- **Integrations**: Add support for other email providers, CRMs
- **Performance**: Optimize embedding generation, query speed
- **Documentation**: Improve guides, add tutorials, create videos
- **Testing**: Write unit/integration tests

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What This Means

You are free to:
- Use this software commercially
- Modify the source code
- Distribute the software
- Use it privately

Under the conditions that:
- You include the original license and copyright notice
- The software is provided "as-is" without warranty

---

## Acknowledgments

### Technologies

- **LangChain**: For the excellent RAG framework
- **Supabase**: For providing world-class PostgreSQL hosting
- **n8n**: For the powerful workflow automation platform
- **OpenRouter**: For unified LLM API access
- **Sentence Transformers**: For semantic embedding models

### Contributors

- **Ahmed Ali** - Initial development and architecture
- **Caster Sport Team** - Domain expertise and policy content

### Special Thanks

- Anthropic Claude for AI assistance
- The open-source community for invaluable tools and libraries

---

## Support & Contact

- **Documentation**: See `TECHNICAL REPORT.pdf` for in-depth details
- **Issues**: Open an issue on GitHub
- **Email**: support@castersport.com
- **Website**: [castersport.com](https://castersport.com)

---

## Roadmap

### Planned Features

- [ ] Multi-channel support (WhatsApp, Telegram, live chat)
- [ ] Voice-to-text integration for phone support
- [ ] Advanced analytics dashboard
- [ ] A/B testing for response quality
- [ ] Customer satisfaction scoring (CSAT)
- [ ] Multilingual expansion (French, Spanish, German)
- [ ] Integration with inventory management systems
- [ ] Automated follow-up scheduling
- [ ] Sentiment analysis for priority routing
- [ ] Knowledge base article recommendations

### Version History

- **v1.0** (Current): Core RAG + n8n automation
- **v0.9**: Beta testing with sample data
- **v0.5**: Initial RAG API implementation
- **v0.1**: Proof of concept

---

<p align="center">
  <strong>Built with ❤️ for exceptional customer service</strong>
</p>

<p align="center">
  <a href="#table-of-contents">Back to Top ↑</a>
</p>
