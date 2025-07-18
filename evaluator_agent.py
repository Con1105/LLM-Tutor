from openai import OpenAI

# Replace with your actual API key
client = OpenAI(api_key="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")  # Replace with your actual key or use env var


def create_quiz_from_lesson(file_path):
    """
    Step 1: Generates a quiz based on the lesson file.

    Parameters:
    - file_path: Path to the lesson file (text format).
    - num_questions: Number of questions to generate (default: 5).

    Returns:
    - A string containing the quiz questions.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lesson_data = f.read()

    system_prompt = """
You are a quiz creator AI.
Given a lesson and Q&A log, create a quiz that thoroughly tests understanding of the concept.

Instructions:
- Emphasize the lesson section (most important).
- Use Q&A for deeper or clarifying insights.
- Include any exercises of the following types (not all need to be included):
  - Multiple Choice Questions (MCQs)
  - Open-ended
  - Application-based or critical thinking questions
- Return the quiz as a numbered list.
- Do NOT include answers.
"""

    user_prompt = f"""
Lesson and Q/A:
-------------------
{lesson_data}

Create a quiz that takes approximately 10 minutes to complete.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()



def evaluate_quiz_answers(file_path, quiz_text, student_answers):
    """
    Step 2: Evaluates student's answers against the original lesson.

    Parameters:
    - file_path: Path to the lesson file used to generate the quiz.
    - student_answers: Student's answers to the quiz as a string.

    Returns:
    - A detailed evaluation of each answer and a final score (0–100).
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lesson_data = f.read()

    system_prompt = """
You are an expert tutor AI.

Evaluate the student's answers to a quiz based on the provided lesson and Q&A. Score their understanding from 0 to 100.

Instructions:
- Be strict but fair.
- If a question is not answered, mark it as 0.
- For each question:
  - Explain if the answer is correct or not.
  - Give brief feedback.
  - Optionally assign a score per question.
- At the end, give an overall percentage score (out of 100) that reflects their understanding.
- Use the lesson content as the primary ground truth.
"""

    user_prompt = f"""
Lesson and Q/A:
-------------------
{lesson_data}

Quiz:
-------------------
{quiz_text}

Student's Answers:
-------------------
{student_answers}

Evaluate and return feedback + score.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
