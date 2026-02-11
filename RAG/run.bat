@echo off
cd /d "%~dp0"
echo Installing/updating packages for current Python...
py -m pip install -q flask langchain-core langchain-community langchain-openai langchain-huggingface langchain-text-splitters faiss-cpu sentence-transformers python-dotenv
echo.
echo Starting Caster Sport RAG API...
py rag_server.py
pause
