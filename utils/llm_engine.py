import ollama


class LLMEngine:
    """
    Uses a local Ollama model to answer questions
    using retrieved context from FAISS.
    """

    def __init__(self, model="qwen2.5:7b"):
        self.model = model

    def ask(self, question, context):

        prompt = f"""
You are an expert AI research assistant.

Answer ONLY using the supplied research paper context.

If the answer is not present in the context, reply:

"Information not found in the uploaded paper."

Be concise.
Be technically accurate.
Do not hallucinate.

==========================
RESEARCH PAPER
==========================

{context}

==========================
QUESTION
==========================

{question}

==========================
ANSWER
"""

        response = ollama.chat(

    model=self.model,

    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],

    options={
        "temperature": 0.2,
        "num_predict": 180
    }

)

        return response["message"]["content"]