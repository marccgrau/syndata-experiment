import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(layout="wide", page_title="Reale vs Synthetische Konversationen", page_icon="🤖")

st.title("Vielen Dank!")
st.write("Vielen Dank für Ihre Teilnahme an unserem Experiment. Ihre Antworten sind wertvoll für unsere Forschung.")
st.write("Folgend finden Sie den Code für Prolific, um Ihre Teilnahme zu bestätigen:")
st.write(f"### {st.secrets['PROLIFIC_CODE'] if st.secrets['PROLIFIC_CODE'] else os.getenv('PROLIFIC_CODE')}")
st.write("Wenn Sie den Code kopiert haben, können Sie diese Seite schließen.")
