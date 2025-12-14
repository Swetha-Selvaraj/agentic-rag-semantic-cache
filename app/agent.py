import json
from .llm import generate
from .vector_store import search_internal
from .web_search import web_search
import json
import re

SYSTEM_PROMPT = """
You are a COMPANY AI ASSISTANT responsible ONLY for TOOL PLANNING.

────────────────────────────────
AVAILABLE TOOLS
────────────────────────────────

You may use ONLY the following tools:

1) vector_search
   Description:
   - Searches INTERNAL company knowledge stored 
   - Includes company policies, internal documentation, and trusted data

   Arguments:
   - query (string): the user question to search for

2) web_search
   Description:
   - Searches PUBLIC internet information
   - Used for general, external, or up-to-date knowledge

   Arguments:
   - query (string): the user question to search for


────────────────────────────────
RESPONSE FORMAT (MANDATORY)
────────────────────────────────

You MUST respond with EXACTLY this JSON structure.
Do NOT include explanations, comments, or extra text.

{
  "tools": [
    {
      "name": "vector_search | web_search",
      "arguments": {
        "query": "string"
      }
    }
  ]
}

────────────────────────────────
RULES (NON-NEGOTIABLE)
────────────────────────────────

- Internal company knowledge is ALWAYS authoritative.
- NEVER override internal knowledge with web information.
- ALWAYS attempt vector_search FIRST.
- Use web_search ONLY if internal search is insufficient or empty.
- NEVER invent new tool names.
- NEVER change the JSON structure.
- If unsure which tool to use, default to web_search.
- Output JSON ONLY.




"""

def extract_json(text: str):
    """
    Safely extract the FIRST JSON object from LLM output
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in LLM output")

    return json.loads(match.group())


def plan(question, memory):
    prompt = f"""
{SYSTEM_PROMPT}

Conversation:
{memory}

Question:
{question}

Respond ONLY with valid JSON.
"""
    text = generate(prompt)
    return extract_json(text)


def execute(plan):
    context = []
    used_internal = False

    for t in plan["tools"]:
        if t["name"] == "vector_search":
            results = search_internal(t["arguments"]["query"])
            if results:
                context += results
                used_internal = True

        elif t["name"] == "web_search":
            context += web_search(t["arguments"]["query"])

    # 🔁 FALLBACK: internal empty → web search
    if not used_internal:
        context += web_search(plan["tools"][0]["arguments"]["query"])

    return "\n".join(context)


def answer(question, context, memory):
    prompt = f"""
Conversation:
{memory}

Context:
{context}

Question:
{question}

Answer using internal policies when available:
"""
    return generate(prompt)
