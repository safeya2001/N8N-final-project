#!/usr/bin/env python3

import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify

app = Flask(__name__)


_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        from langchain_community.document_loaders import TextLoader, DirectoryLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        policies_dir = os.path.join(SCRIPT_DIR, "policies")
        if not os.path.isdir(policies_dir):
            return None
        loader = DirectoryLoader(policies_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        docs = loader.load()
        if not docs:
            return None
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        splits = splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(splits, embeddings)
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return _retriever


def get_answer(question: str, retriever):
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """أنت مساعد ذكي وودود لـ Caster Sport (متجر/منصة رياضية). مهمتك كتابة رد إيميل احترافي ومرتب.

قواعد المحتوى:
1) إذا السؤال عن سياساتنا أو خدماتنا (ترجيع، شحن، تلف، إلغاء، استرداد، حساب، تواصل): أجب من Context فقط بوضوح وترتيب.
2) إذا السؤال عن منتجات لا نبيعها (مثل سيارات، عقارات): اذكر بوضوح أننا لا نبيع ذلك، قدّم بديلنا (متجر رياضة)، وادعُ العميل للتواصل: support@castersport.com أو واتساب الدعم 0791485324. كن دافئاً وواضحاً.
3) إذا طلب قائمة منتجات أو كتالوج: اذكر أن القائمة على الموقع وادعُه للتواصل للطلب أو الاستفسار.
4) أجب بلغة المستخدم (عربي أو إنجليزي).

تنسيق الإخراج (مهم جداً):
- السطر الأول فقط: موضوع الإيميل المقترح (قصير، بدون "Subject:" أو "موضوع:")، مثال: "رد على استفسارك - Caster Sport" أو "بخصوص بيع السيارات".
- سطر فارغ.
- ثم نص الرسالة بهذا الشكل:
  • تحية مناسبة (مرحباً / عزيزي العميل،)
  • فقرة أو أكثر واضحة ومرتبة للإجابة.
  • ختام مهني (مع تحياتنا، فريق Caster Sport أو Best regards, Caster Sport Team).

اجعل الرد يبدو من مساعد ذكي: واضح، مرتب، وودود.
Context: {context}"""),
        ("human", "{question}")
    ])
    llm = ChatOpenAI(
        model="google/gemini-2.0-flash-001",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.2
    )
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(question)


def _parse_email_response(raw: str):
    """يستخرج من أول سطر موضوع الإيميل وباقي النص جسد الرسالة."""
    raw = (raw or "").strip()
    if not raw:
        return "رد على استفسارك - Caster Sport", ""
    lines = raw.split("\n")
    subject = (lines[0] or "").strip()
    if not subject:
        subject = "رد على استفسارك - Caster Sport"
    # إزالة أي بادئة مثل "Subject:" أو "موضوع:"
    for prefix in ("subject:", "موضوع:", "re:"):
        if subject.lower().startswith(prefix):
            subject = subject[len(prefix):].strip()
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
    if not body:
        body = raw
        subject = "رد على استفسارك - Caster Sport"
    return subject, body


@app.route("/ask", methods=["POST"])
def ask():
    try:
        body = request.get_json(force=True, silent=True) or {}
        question = (body.get("question") or body.get("emailBody") or "").strip()
        email_from = body.get("emailFrom") or body.get("email_from") or ""
        email_subject = body.get("emailSubject") or body.get("email_subject") or ""
        chat_id = body.get("chatId") or body.get("chat_id") or ""
        if not question:
            return jsonify({"answer": "", "error": "no_question", "emailFrom": email_from, "emailSubject": email_subject or "Chat", "chatId": chat_id}), 400
        retriever = get_retriever()
        if retriever is None:
            return jsonify({"answer": "لم يتم العثور على السياسات.", "error": "no_policies", "emailFrom": email_from, "emailSubject": email_subject or "Chat", "chatId": chat_id})
        raw_answer = get_answer(question, retriever)
        subject, email_body = _parse_email_response(raw_answer)
        # إذا الاستفسار من إيميل (موضوع حقيقي) نستخدم Re: الموضوع، وإلا نستخدم موضوع الـ AI (مثل Telegram)
        if email_subject and (email_subject.strip() != "" and email_subject.strip() != "Chat"):
            subject = f"Re: {email_subject.strip()}" if not email_subject.strip().lower().startswith("re:") else email_subject.strip()
        return jsonify({"answer": email_body, "error": "", "emailFrom": email_from, "emailSubject": subject, "chatId": chat_id})
    except Exception as e:
        return jsonify({"answer": "", "error": str(e), "emailFrom": "", "emailSubject": "Chat", "chatId": ""}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("RAG_SERVER_PORT", "5050"))

    print("Loading RAG (policies + embeddings)...")
    try:
        get_retriever()
        print("RAG ready.")
    except Exception as e:
        print(f"RAG pre-load warning: {e}")
    print(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
