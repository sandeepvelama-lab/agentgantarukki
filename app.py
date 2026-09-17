import os
import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Agent Rukki",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ This is Agent Ganta Rukki")
st.caption("Upload an audio file or record audio, I can transcribe it for you.")

st.markdown(
    """
    <style>
    /* Remove sidebar padding */
    [data-testid="stSidebar"] > div:first-child {
        padding-left: 0;
        padding-right: 0;
        padding-top: 0;
    }

    /* Make image fill sidebar width */
    [data-testid="stSidebar"] img {
        width: 100% !important;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    # st.header("Agent")
    st.markdown(
        """
        <style>
        /* Make the sidebar use the full screen height */
        [data-testid="stSidebar"] > div:first-child {
            padding: 0 !important;
            height: 100vh !important;
        }

        /* Make the image fill the entire sidebar */
        [data-testid="stSidebar"] img {
            width: 100% !important;
            height: 100vh !important;
            object-fit: fill !important;
            display: block;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image("Anji.jpg", use_container_width=True)
    # st.image(
    #     "Anji.jpg",
    #     use_container_width=True
    # )
    # model = "gpt-5.5" # "gpt-4o-mini-transcribe"
    # language = ""
model = "gpt-5.5" # "gpt-4o-mini-transcribe"
language = ""
client = OpenAI(api_key="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")

st.subheader("1. Choose audio")

uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "ogg", "flac"],
)

st.write("**Or record from your microphone:**")
recorded_audio = st.audio_input("Record audio")

audio_source = uploaded_file if uploaded_file is not None else recorded_audio

if audio_source:
    st.audio(audio_source)

    st.subheader("2. Transcribe")

    if st.button("🚀 Transcribe Audio", type="primary", use_container_width=True):
        suffix = Path(getattr(audio_source, "name", "recording.wav")).suffix.lower()

        if not suffix:
            suffix = ".wav"

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(audio_source.getvalue())
                temp_path = tmp.name

            with st.spinner("Transcribing audio..."):
                with open(temp_path, "rb") as audio_file:
                    kwargs = {
                        "model": model,
                        "file": audio_file,
                    }

                    if language.strip():
                        kwargs["language"] = language.strip()

                    transcription = client.audio.transcriptions.create(**kwargs)

            text = transcription.text

            st.subheader("3. Transcription")
            st.text_area(
                "Text",
                value=text,
                height=300,
                label_visibility="collapsed",
            )

            st.download_button(
                "⬇️ Download transcript",
                data=text,
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as exc:
            # st.error(f"Transcription failed: {exc}")
            st.error(f"Transcription failed: Paisal evadisthad ra??? Fukat la service kavalna...Asale nenu Ganta Rukki ni.")

        finally:
            try:
                os.remove(temp_path)
            except (NameError, FileNotFoundError):
                pass

st.divider()
# st.caption("Your audio is sent to the OpenAI API for transcription. Keep your API key private.")
