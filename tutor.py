from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # Replace with your actual key or use env var

def tutor_agent(concept, chat_history):
    """
    AI Tutor agent that gives a textbook-style lesson as in academic books and then answers student questions.

    Parameters:
    - concept (str): The main concept/topic to teach.
    - chat_history (list of dict): A list of messages in the format {"role": ..., "content": ...}

    Returns:
    - assistant_response (str): Tutor's response.
    """
    
    # Check if it's the first interaction
    is_first = len(chat_history) == 1 and chat_history[0]["role"] == "user"

    system_prompt = f"""You are an expert AI tutor who teaches university-level students using a textbook-like approach.

    First prompt should be a long text analyzing **{concept}** in the format of an academic book.

    The chapters should be structured with Titles (not too big) and explain in the form of paragraphs.
    If applicable, give example of applications (e.g. if the concept is Pythagoreum theorem, giva e simple solved ecercise)
    If applicable, give reference to papers etc.
    If there is too much to teach, ask student what to analyze first in more detail.
    
    After the first prompt, the student will ask questions about the lesson, expand or clarify the relevant part using the context previous prompts and responses.
    
"""

    messages = [{"role": "system", "content": system_prompt}] + chat_history

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.2,
        stream=True
    )

    full_reply = ""
    placeholder = st.empty()

    for chunk in response:
        content_piece = chunk.choices[0].delta.content
        if content_piece:
            full_reply += content_piece
            placeholder.markdown(full_reply + "▌")

    placeholder.markdown(full_reply)
    return full_reply.strip()
