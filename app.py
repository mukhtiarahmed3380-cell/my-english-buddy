import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from google import genai
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS

load_dotenv()

st.set_page_config(
    page_title="My English Buddy",
    page_icon="📚",
    layout="centered"
)

st.title("📚 My English Buddy")
st.write("Your friendly English-speaking partner!")
st.write("Baat karo, English seekho aur confidence barhao.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key nahi mili. Streamlit Advanced Settings -> Secrets mein GEMINI_API_KEY check karo.")
    st.stop()

client = genai.Client(api_key=api_key)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hi friend! 😊 How was your day today? "
                "Tell me in English or Roman Urdu."
            )
        }
    ]

# Chat history ko display karna
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("🎤 Talk to your AI friend")
st.caption("Microphone dabao, bolo, aur phir recording stop karo.")

# Mobile and Browser compatible voice recorder
spoken_text = speech_to_text(
    language="en",
    start_prompt="🎙️ Start speaking",
    stop_prompt="⏹️ Stop recording",
    just_once=True,
    key="voice_input"
)

typed_text = st.text_input(
    "Ya apna message yahan likho:",
    placeholder="Example: Aaj mujhe college nahi jana."
)

if st.button("Send message 💬"):
    user_text = typed_text.strip() or (spoken_text or "").strip()

    if not user_text:
        st.warning("Pehle bolo ya message type karo.")
    else:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_text}
        )

        instructions = """
You are a friendly female AI friend and English conversation partner.
The learner is at intermediate level and understands Roman Urdu.

Talk naturally like a supportive friend. Mix simple English and Roman Urdu
when useful. Ask one follow-up question so the conversation continues.

When the learner writes or speaks in Roman Urdu, give a natural English
version they could use in real life.

When the learner uses English, gently correct important mistakes and
briefly explain them in Roman Urdu. Do not over-correct or embarrass them.

Encourage the learner to answer in English. Keep replies conversational,
not like a long textbook lesson. Ask only one question at a time.
"""
        history = st.session_state.chat_history[-12:]
        conversation = "\n".join(
            f"{m['role']}: {m['content']}" for m in history
        )

        try:
            with st.spinner("Your AI friend is thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=instructions + "\n\nConversation:\n" + conversation
                )

            answer = response.text or "Sorry friend, please try again."
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

            st.rerun()

        except Exception as e:
            st.error("AI response nahi mil saka.")
            st.code(str(e))

# AI ki aakhri baat ko sunne ka button
if st.session_state.chat_history:
    last_answer = next(
        (
            m["content"]
            for m in reversed(st.session_state.chat_history)
            if m["role"] == "assistant"
        ),
        ""
    )

    if st.button("🔊 Listen to AI friend"):
        try:
            with st.spinner("Voice tayyar ho rahi hai..."):
                tts = gTTS(text=last_answer, lang="en")
                with tempfile.NamedTemporaryFile(
                    suffix=".mp3", delete=False
                ) as audio_file:
                    audio_path = audio_file.name

                tts.save(audio_path)

                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")

                os.remove(audio_path)

        except Exception as e:
            st.error("Voice generate nahi hui. Internet connection check karo.")
            st.code(str(e))

if st.button("🔄 Start a new conversation"):
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hi friend! 😊 How was your day today? "
                "Tell me in English or Roman Urdu."
            )
        }
    ]
    st.rerun()

st.caption("Practice daily. Small steps, big progress! 💪")
