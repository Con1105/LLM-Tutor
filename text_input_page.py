import streamlit as st
from tutor import tutor_agent
from evaluator_agent import create_quiz_from_lesson, evaluate_quiz_answers

st.set_page_config(page_title="Knowledge Graph Curriculum Customizer", layout="wide")
st.title("Knowledge Graph Tutor Session")
st.write("Enter a concept to start a personalized lesson. Ask follow-up questions below.")

# Initialize session state
if 'lesson_displayed' not in st.session_state:
    st.session_state.lesson_displayed = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'qa_log' not in st.session_state:
    st.session_state.qa_log = []
if 'concept' not in st.session_state:
    st.session_state.concept = ""
if 'quiz' not in st.session_state:
    st.session_state.quiz = ""
if 'quiz_feedback' not in st.session_state:
    st.session_state.quiz_feedback = ""
if 'student_response' not in st.session_state:
    st.session_state.student_response = ""
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False


# Start the lesson
if not st.session_state.lesson_displayed:
    concept = st.text_input("Enter a concept to learn:")
    if concept and not st.session_state.get("lesson_text"):
        st.session_state.concept = concept
        initial_prompt = f"Teach me about {concept}."
        initial_history = [{"role": "user", "content": initial_prompt}]

        # Call agent to get the lesson but DO NOT show anything yet
        lesson = tutor_agent(concept, initial_history)

        # Save to state and file
        st.session_state.lesson_text = lesson
        st.session_state.lesson_displayed = True
        with open(f"{concept}_lesson.txt", "w", encoding="utf-8") as f:
            f.write(f"### Concept: {concept}\n\nLesson:\n{lesson}\n\nQ/A:\n")

        # Trigger rerun to show lesson in clean UI
        st.rerun()

# Show the full lesson cleanly (no icons, only once)
if st.session_state.get("lesson_displayed") and st.session_state.get("lesson_text"):
    st.markdown(st.session_state.lesson_text)

# Show full chat history
if st.session_state.lesson_displayed:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_question = None
    if not st.session_state.quiz:
        user_question = st.chat_input("Ask a question or type 'continue' to learn more...")

    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            answer = tutor_agent(st.session_state.concept, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.qa_log.append({"Q": user_question, "A": answer})

        with open(f"{st.session_state.concept}_lesson.txt", "a", encoding="utf-8") as f:
            f.write(f"Q: {user_question}\nA: {answer}\n\n")

        st.rerun()

# Quiz Generation Trigger
if st.session_state.lesson_displayed:
    if st.button("I'm Ready for Quiz"):
        with open(f"{st.session_state.concept}_lesson.txt", "a", encoding="utf-8") as f:
            f.write("\n---\nFull Q/A Chat Log:\n")
            for entry in st.session_state.qa_log:
                f.write(f"Q: {entry['Q']}\nA: {entry['A']}\n\n")

        lesson_file_path = f"{st.session_state.concept}_lesson.txt"
        with st.spinner("Creating Quiz..."):
            quiz = create_quiz_from_lesson(lesson_file_path)
        st.session_state.quiz = quiz
        st.session_state.quiz_feedback = ""
        st.session_state.student_response = ""
        st.session_state.quiz_submitted = False
        st.rerun()  # Rerun to render clean quiz section

# Quiz Display and Submission
if st.session_state.quiz:
    st.subheader("Quiz Time!")
    st.info("A custom quiz has been generated based on your lesson and Q&A. Please answer below.")
    st.markdown(f"**Quiz:**\n\n{st.session_state.quiz}")

    if st.session_state.quiz_submitted:
        st.markdown("**Your Answers:**")
        st.text_area("Your answers:", value=st.session_state.student_response, height=300, disabled=True)
        st.subheader("Feedback & Score")
        st.markdown(st.session_state.quiz_feedback)
    else:
        student_response = st.text_area("Your answers:", height=300)
        if st.button("Submit Answers"):
            lesson_file_path = f"{st.session_state.concept}_lesson.txt"
            with st.spinner("⏳ Wait for feedback..."):
                feedback = evaluate_quiz_answers(lesson_file_path, st.session_state.quiz, student_response)

            st.session_state.quiz_feedback = feedback
            st.session_state.student_response = student_response
            st.session_state.quiz_submitted = True
            st.rerun()




        # # Reset session
        # st.session_state.lesson_displayed = False
        # st.session_state.messages = []
        # st.session_state.qa_log = []
        # st.session_state.concept = ""

