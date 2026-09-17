import os
import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Audio to Text - OpenAI",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ Audio to Text")
st.caption("Upload an audio file or record audio, then transcribe it with the OpenAI Python SDK.")

with st.sidebar:
    st.header("Settings")
    model = "gpt-5.5" # "gpt-4o-mini-transcribe"
    language = ""
    # model = st.selectbox(
    #     "Transcription model",
    #     ["gpt-4o-mini-transcribe", "gpt-4o-transcribe", "whisper-1"],
    #     index=0,
    # )
    # language = st.text_input(
    #     "Language (optional)",
    #     value="",
    #     placeholder="e.g. en",
    #     help="ISO-639-1 language code. Leaving this blank lets the transcription model detect it.",
    # )
    # api_key = st.text_input(
    #     "OpenAI API key",
    #     value="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", # os.getenv("OPENAI_API_KEY", ""),
    #     type="password",
    #     help="For local use you can enter it here, or set OPENAI_API_KEY in your environment.",
    # )

# if not api_key:
#     st.info("Enter your OpenAI API key in the sidebar, or set the OPENAI_API_KEY environment variable.")
#     st.stop()

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
            st.error(f"Transcription failed: {exc}")

        finally:
            try:
                os.remove(temp_path)
            except (NameError, FileNotFoundError):
                pass

st.divider()
st.caption("Your audio is sent to the OpenAI API for transcription. Keep your API key private.")
