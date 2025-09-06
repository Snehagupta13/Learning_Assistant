import streamlit as st
from backend.theme import apply_theme  
apply_theme()
from backend.generator import generate_doc
from backend.quiz import generate_quiz, evaluate_quiz
from backend.rag import fetch_context
from backend.utils import save_to_pdf
from backend.progress import load_progress, log_attempt, get_badges
import pandas as pd
import streamlit.components.v1 as components
from backend.gamify import gamify_doc
import plotly.express as px



st.set_page_config(page_title="AI Learning Assistant", layout="wide")
st.title("📘 AI-Powered Interactive Learning Assistant")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Pre-Class Doc", "Post-Class Doc", "Quiz","Progress", "Gamify"])

if page == "Home":
    st.subheader("Welcome 👋")
    st.write("Enter a topic, generate pre-class & post-class study docs, and take quizzes!")

elif page == "Pre-Class Doc":
    topic = st.text_input("Enter Topic for Pre-Class Document")
    length = st.selectbox("Select Document Length", ["short", "medium", "detailed"])

    if st.button("Generate Pre-Class Document"):
        context = fetch_context(topic)
        # ✅ generate_doc now only returns text
        doc_text = generate_doc(topic, doc_type="pre", length=length, context=context)

        # Show the generated text only
        st.markdown(doc_text)

        # ✅ Only pass the text to save_to_pdf
        st.download_button(
            "Download Pre-Class PDF",
            save_to_pdf(doc_text, f"{topic}_pre.pdf"),
            file_name=f"{topic}_pre.pdf"
        )


elif page == "Post-Class Doc":
    topic = st.text_input("Enter Topic for Post-Class Document")
    length = st.selectbox("Select Document Length", ["short", "medium", "detailed"])

    if st.button("Generate Post-Class Document"):
        context = fetch_context(topic)
        # ✅ generate_doc now only returns text
        doc_text = generate_doc(topic, doc_type="post", length=length, context=context)

        # Show the generated text only
        st.markdown(doc_text)

        # ✅ Only pass the text to save_to_pdf
        st.download_button(
            "Download Post-Class PDF",
            save_to_pdf(doc_text, f"{topic}_post.pdf"),
            file_name=f"{topic}_post.pdf"
        )




elif page == "Quiz":
    topic = st.text_input("Enter Topic for Quiz")
    difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

    # Generate quiz only when button is pressed
    if st.button("Generate Quiz"):
        quiz, answers = generate_quiz(topic, difficulty=difficulty)
        if quiz:  # only store if quiz was generated
            st.session_state["quiz"] = quiz
            st.session_state["answers"] = answers
        else:
            st.warning("⚠️ No quiz generated. Try again or check backend.")



    # Display quiz if available
    if "quiz" in st.session_state and st.session_state["quiz"]:
        st.subheader("Quiz")
        user_answers = {}

        for idx, q in enumerate(st.session_state["quiz"], 1):
            st.write(f"**Q{idx}: {q['question']}**")
            if q["type"] == "mcq":
                user_answers[idx] = st.radio(
                    f"Choose option for Q{idx}:", 
                    q["options"], 
                    key=f"q{idx}"
                )
            else:  # fill-in-the-blank
                user_answers[idx] = st.text_input(
                    f"Your answer for Q{idx}:", 
                    key=f"q{idx}"
                )

        if st.button("Submit Answers"):
            score, feedback = evaluate_quiz(user_answers, st.session_state["answers"])
            st.success(f"Your Score: {score}")
            st.markdown("### Feedback")
            st.markdown(feedback)

            # ✅ Log attempt
            try:
                scored, total = score.split("/")
                log_attempt(topic, difficulty, int(scored), int(total))
            except:
                pass

elif page == "Progress":
    st.subheader("📊 Your Progress History")

    progress_data = load_progress()
    if not progress_data:
        st.info("No progress yet. Take some quizzes to see your history!")
    else:
        df = pd.DataFrame(progress_data)
        st.dataframe(df)

        avg_score = df["score"].sum() / df["total"].sum() * 100
        st.metric("Average Score", f"{avg_score:.1f}%")

        st.markdown("### Topics Attempted")
        topic_counts = df["topic"].value_counts()
        st.bar_chart(topic_counts)

        # --- Extra Dashboard ---
        st.markdown("### Detailed Dashboard")
        df["accuracy"] = df["score"] / df["total"] * 100

        # Pie chart
        fig_pie = px.pie(
            df, names="topic", values="accuracy",
            title="Accuracy by Topic", hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Bar chart
        fig_bar = px.bar(
            df, x="topic", y="score", color="difficulty", text="score",
            title="Scores by Topic and Difficulty"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Badges
        st.subheader("🏅 Your Badges")
        badges = get_badges(progress_data)
        if badges:
            st.write(" ".join(badges))
        else:
            st.write("No badges yet, keep practicing!")


elif page == "Gamify":
    st.title("Gamified Interactive Learning")

    topic = st.text_input("Topic", value="Arrays in JavaScript")
    length = st.selectbox("Length", ["short", "medium", "long"], index=1)
    context = st.text_area("Additional Context (optional)", height=50)

    if st.button("Generate and Render Document"):
        with st.spinner("Generating your gamified learning document..."):
            html_content = gamify_doc(topic, length, context)

        st.header("Your Interactive Learning Document")
        components.html(html_content, height=800, scrolling=True)
