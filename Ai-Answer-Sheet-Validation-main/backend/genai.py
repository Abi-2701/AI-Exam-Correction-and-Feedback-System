import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key="AIzaSyDbtoVg7zy5YWOGQ2jk1yU7U6Vg3D4Jd9M")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    enum = [],
    required = ["question_no"],
    properties = {
      "question_no": content.Schema(
        type = content.Type.STRING,
      ),
    },
  ),
  "response_mime_type": "application/json",
}

def identify_question_no(questions,answer):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=f"I will give the answer and you need to match the answer with below keywords and need to provide the matching question_no\n\n{questions}",
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(answer)
    return response.text