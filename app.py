import streamlit as st

# Page configuration
st.set_page_config(
    page_title="LLM",
    layout="centered"
)

# Application title
st.title("AI Interview")
st.caption("Practice and Prepare for your placement")
st.caption("Launched by Akshaya")

# Import Groq
try:
    from groq import Groq
except ImportError:
    st.error("Groq package is not installed.")
    st.stop()

# API configuration
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

st.success("Groq API connected successfully!")

st.write("Welcome to your AI Interview Assistant.")

# Job role
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineer",
        "Data Analyst",
        "Cyber Security",
        "Software Developer",
        "Others"
    ]
)

if role == "Others":
    role = st.text_input("Enter your Job Title")

# Model selection
model = st.selectbox(
    "Choose your model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)

# Difficulty level
level = st.selectbox(
    "Choose your level",
    ["Beginner", "Intermediate", "Advanced"]
)

# Activity selection
mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve Answers"
    ]
)

# Initialize variables
topic = ""
count = 5
question = ""
answer = ""

if mode == "Generate Questions":
    count = st.slider("Number of Questions", 1, 10, 5)

elif mode == "Generate Code Questions":
    topic = st.selectbox(
        "Select Topic",
        ["Python", "C++", "C", "DSA", "Aptitude", "Java"]
    )
    count = st.slider("Number of Questions", 1, 10, 5)

else:
    question = st.text_area("Enter Interview Question Here")
    answer = st.text_area("Enter Your Answer", height=160)

# Generate response
if st.button("Generate AI Response", type="primary"):

    if mode in ["Evaluate Answers", "Improve Answers"]:
        if not question.strip() or not answer.strip():
            st.warning("Please enter both the question and answer.")
            st.stop()

    if mode == "Generate Questions":
        task = (
            f"Generate {count} frequently asked interview questions. "
            "Include situation-based and theory questions."
        )

    elif mode == "Generate Code Questions":
        task = (
            f"Generate {count} frequently asked coding questions "
            f"on {topic}. Difficulty: {level}. "
            "Provide hints and expected solutions."
        )

    elif mode == "Evaluate Answers":
        task = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Evaluate the answer, identify mistakes, "
            "and suggest improvements."
        )

    elif mode == "Improve Answers":
        task = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Improve the answer and highlight important points."
        )

    background = (
        f"Job Role: {role}\n"
        f"Difficulty Level: {level}\n"
    )

    with st.spinner("Generating your answer..."):

        try:
            req = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Act as an expert technical interviewer "
                            "and HR professional."
                        )
                    },
                    {
                        "role": "user",
                        "content": background + task
                    }
                ],
                temperature=0.7,
                max_tokens=1800
            )

            output = req.choices[0].message.content

            st.subheader("AI Response")
            st.markdown(output)

            st.download_button(
                "Download Response",
                output,
                file_name="Interview_Response.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"API connection was unsuccessful: {e}")
            st.info("Please check your API key and rate limits.")

st.caption("Powered by Streamlit and Groq API")
