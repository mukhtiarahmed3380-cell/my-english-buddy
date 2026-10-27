
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="My English Buddy",
    page_icon="📚",
    layout="centered"
)

st.title("📚 My English Buddy")
st.write("Your personal English learning partner!")
st.write("Roman Urdu mein likho aur English seekho.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key nahi mili. Apni .env file check karo.")
    st.stop()

client = genai.Client(api_key=api_key)

urdu_text = st.text_area(
    "Apni baat Roman Urdu ya English mein likho:",
    placeholder="Example: Mujhe English seekhni hai."
)

if st.button("Help me learn"):
    if urdu_text.strip():
        prompt = f"""
You are my friendly English tutor.
The student is a beginner and understands Roman Urdu.

For the following message:
1. Give a natural English translation.
2. Explain its meaning in simple Roman Urdu.
3. Correct any English mistakes gently.
4. Give one useful example sentence in English with Roman Urdu meaning.

Keep the response simple and encouraging.

Student's message: {urdu_text}
"""
        try:
            with st.spinner("Tumhara English tutor soch raha hai..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
            st.subheader("📖 Let's Learn English")
            st.markdown(response.text)
        except Exception as e:
            st.error("AI response nahi mil saka. Error:")
            st.code(str(e))
    else:
        st.warning("Pehle kuch likho!")

st.caption("Step by step, we will improve your English. 💪")
