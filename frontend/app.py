import streamlit as st
import requests
import json
import tempfile
import re
from gtts import gTTS

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Adhigam Physics Tutor (AI)", layout="centered")
st.title("📘 Bhojpuri Physics Tutor (AI-Powered)")
st.markdown("Speak a physics question. The AI teacher will explain the concept step by step with text, audio, diagram, animation, and native examples — all in Bhojpuri.")


def clean_js_code(gpt_output: str) -> str:
    cleaned = re.sub(r"\[DIAGRAM_START\]|\[DIAGRAM_END\]", "", gpt_output)
    cleaned = re.sub(r"```(javascript|js)?\s*", "", cleaned)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()


def speak_text_streamlit(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_bytes = fp.read()
        st.audio(fp.name, format="audio/mp3")



def render_p5_code(js_code: str):
    html_template = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <script src=\"https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.6.0/p5.js\"></script>
        <style>
            html, body {{ margin: 0; padding: 0; background: white; overflow: hidden; width: 100%; height: 100%; }}
            canvas {{ display: block; margin: auto; background: transparent; }}
        </style>
    </head>
    <body>
        <script type=\"text/javascript\">
            {js_code}
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_template, height=600, scrolling=False)


if "initialized" not in st.session_state:
    st.session_state.initialized = False

prompt = "what is third law of motion?"
st.markdown(f"### 🗣️ Transcribed Text: {prompt}")

if prompt and not st.session_state.initialized:
    with st.spinner("🤖 Explaining the concept step by step..."):
        explain_res = requests.post(f"{BACKEND_URL}/explain", json={"prompt": prompt})
        res_json = explain_res.json()

        if "error" in res_json:
            st.error(f"❌ Azure returned an error: {res_json['error']}")
            st.stop()

        st.session_state.explanation = res_json.get("explanation", "")
        st.session_state.quiz_json = res_json.get("quiz", [])

        diagram_res = requests.post(f"{BACKEND_URL}/generate_diagram_code", json={"prompt": prompt})
        diagram_json = diagram_res.json()
        st.session_state.js_code = clean_js_code(diagram_json.get("p5js", ""))
        st.session_state.diagram_explanation = diagram_json.get("explanation", "")

        st.session_state.initialized = True

if st.session_state.initialized:
    st.markdown("### 📖 Step 1: Explanation in Bhojpuri")
    st.markdown(st.session_state.explanation)
    speak_text_streamlit(st.session_state.explanation)

    st.markdown("### 🖼️ Step 2: Diagram Animation")
    render_p5_code(st.session_state.js_code)

    st.markdown("### 📘 Diagram Explanation")
    st.markdown(st.session_state.diagram_explanation)
    speak_text_streamlit(st.session_state.diagram_explanation)

    st.markdown("### 🧠 Step 5: Test Yourself with Quiz")

    quiz = st.session_state.quiz_json  # Read once

    for idx, q in enumerate(quiz):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")

        key_radio = f"q{idx}_selected"
        key_show_result = f"q{idx}_show_result"

        # Use session state to persist selection + submission
        if key_radio not in st.session_state:
            st.session_state[key_radio] = None
        if key_show_result not in st.session_state:
            st.session_state[key_show_result] = False

        selected = st.radio("अपना जवाब चुनें:", q["options"], key=key_radio, index=None)

        # Once selected, show result immediately and persist
        if selected is not None:
            st.session_state[key_show_result] = True

        # Show result if previously selected
        if st.session_state[key_show_result]:
            correct = q["answer"]
            if st.session_state[key_radio] == correct:
                st.success("✅ सही जवाब!")
            else:
                st.error(f"❌ गलत। सही जवाब बा: {correct}")



