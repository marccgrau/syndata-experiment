import random
import uuid
from datetime import datetime
from typing import Dict, List

import duckdb
import streamlit as st
from datasets import load_dataset

st.set_page_config(layout="wide", page_title="Reale vs Synthetische Konversationen", page_icon="🤖")


# Load real and synthetic examples
@st.cache_data
def load_examples(dataset_name: str, split: str) -> List[Dict]:
    """Load examples from a Hugging Face dataset."""
    try:
        dataset = load_dataset(dataset_name, split=split)
        return dataset
    except Exception as e:
        st.error(f"Error loading dataset from Hugging Face: {e}")
        return []


real_examples = load_examples("marccgrau/real_calls_dialogsum", "train")
synthetic_examples = load_examples("marccgrau/synthetic_data_final_eval", "train")

# Initialize DuckDB database and table in a file
db_connection = duckdb.connect(database="user_selections.db")

# Create the sequence if it doesn't exist
db_connection.execute("CREATE SEQUENCE IF NOT EXISTS user_selections_seq")

# Create the user selections table if it doesn't exist
db_connection.execute("""
    CREATE TABLE IF NOT EXISTS user_selections (
        id INTEGER DEFAULT nextval('user_selections_seq') PRIMARY KEY,
        timestamp TIMESTAMP,
        user_id TEXT,
        real_example_id TEXT,
        synthetic_example_id TEXT,
        selected_real BOOLEAN,
        model_id TEXT,
        instruct_lang TEXT,
        generation_method TEXT
    )
""")


def get_random_examples() -> List[Dict]:
    """Get one random real example and one random synthetic example, shuffles them, and returns them."""
    real_example = random.choice(real_examples)
    real_example["source"] = "real"
    synthetic_example = random.choice(synthetic_examples)
    synthetic_example["source"] = "synthetic"
    examples = [real_example, synthetic_example]
    random.shuffle(examples)
    return examples


def display_example(example: Dict):
    """Display the conversation example in Streamlit."""
    with st.expander("Chat Transkript", expanded=True):
        for item in example["script"]:
            role = "ai" if str(item["person"]).lower() == "agent" else "user"
            with st.chat_message(role):
                st.markdown(item["text"])


def save_selection_to_db(
    user_id: str,
    real_example_id: str,
    synthetic_example_id: str,
    selected_real: bool,
    model_id: str,
    instruct_lang: str,
    generation_method: str,
):
    """Save the user's selection and example IDs to the DuckDB database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_connection.execute(
        """
        INSERT INTO user_selections (
            timestamp, user_id, real_example_id, synthetic_example_id, selected_real, model_id, instruct_lang, generation_method
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            user_id,
            real_example_id,
            synthetic_example_id,
            selected_real,
            model_id,
            instruct_lang,
            generation_method,
        ),
    )


st.title("Reale vs Synthetische Konversationen")

st.subheader("Aufgabe")
st.write(
    """
    Untenstehend sehen sie zwei verschiedene Konversationsskripte. Lesen sie diese aufmerksam durch.
    Anschliessend beurteilen Sie welche der beiden Konversationen sie eher als real einschätzen würden.
    Es kann jeweils nur ein Beispiel ausgewählt werden.
    Sobald Sie eine Entscheidung getroffen haben, bestätigen Sie Ihre Auswahl mit dem Knopf "Auswahl bestätigen".
    Anschliessend werden zwei neue Beispiele geladen werden, welche erneut beurteilt werden sollen.
    Sobald Sie 10 Beispiele beurteilt haben, werden Sie automatisch weitergeleitet.
    """
)
st.write(
    """
    Personen, Aktientitel, Firmennamen und andere spezifische Informationen wurden in den Konversationen anonymisiert.
    Diese dienen nicht als Indikator für die Echtheit der Konversationen.
    """
)

# Generate a UUID for the user if it doesn't exist
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Initialize the answer counter if it doesn't exist
if "answer_count" not in st.session_state:
    st.session_state.answer_count = 0

if "current_examples" not in st.session_state:
    st.session_state.current_examples = get_random_examples()

examples = st.session_state.current_examples

# Ensure radio button state exists in session state
if "selected_example" not in st.session_state:
    st.session_state.selected_example = None

# Randomly decide which example goes on the left and which on the right
left_example, right_example = examples[0], examples[1]

with st.container():
    col1, col2 = st.columns([2, 2])

    with col1:
        st.header("Beispiel 1")
        display_example(left_example)

    with col2:
        st.header("Beispiel 2")
        display_example(right_example)

# Add a horizontal line to separate the buttons from the examples
st.markdown("---")

# Full-width buttons and radio buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_example = st.radio("Wählen Sie welches Beispiel real ist:", ("Beispiel 1", "Beispiel 2"), key="selected_example")

    def confirm_selection():
        """Save the user's selection and load new examples."""
        if "selected_example" not in st.session_state:
            st.error("Please select one example as real.")
            return

        examples = st.session_state.current_examples
        selected_example = st.session_state.selected_example

        if selected_example == "Beispiel 1":
            real_example = examples[0] if examples[0]["source"] == "real" else examples[1]
            synthetic_example = examples[1] if examples[0]["source"] == "real" else examples[0]
        else:
            real_example = examples[1] if examples[1]["source"] == "real" else examples[0]
            synthetic_example = examples[0] if examples[1]["source"] == "real" else examples[1]

        real_example_id = real_example["call_id"]
        synthetic_example_id = synthetic_example["call_id"]
        selected_real = selected_example == "Beispiel 1" if real_example == examples[0] else selected_example == "Beispiel 2"

        model_id = synthetic_example["model"]
        instruct_lang = synthetic_example["instruct_lang"]
        generation_method = synthetic_example["generation_method"]

        if "user_selections" not in st.session_state:
            st.session_state.user_selections = []
        st.session_state.user_selections.append(
            {
                "real_example_id": real_example_id,
                "synthetic_example_id": synthetic_example_id,
                "selected_real": selected_real,
            }
        )
        save_selection_to_db(
            st.session_state.user_id,
            real_example_id,
            synthetic_example_id,
            selected_real,
            model_id,
            instruct_lang,
            generation_method,
        )
        # Increment the answer counter
        st.session_state.answer_count += 1

        st.success("Selection confirmed. Loading next examples...")
        st.session_state.current_examples = get_random_examples()
        # Reset radio button selection
        st.session_state.selected_example = None

    if st.session_state.answer_count >= 10:
        st.switch_page("pages/2_thankyou.py")
    confirm_button = st.button("Auswahl bestätigen", on_click=confirm_selection, use_container_width=True)
