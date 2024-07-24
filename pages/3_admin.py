import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Reale vs Synthetische Konversationen", page_icon="🤖")

# Initialize DuckDB database and table in a file
db_connection = duckdb.connect(database="user_selections.db")


# Function to load selections from the DuckDB database
def load_selections_from_db():
    """Load all user selections from the DuckDB database."""
    result = db_connection.execute("SELECT * FROM user_selections").fetchall()
    selections = []
    for row in result:
        selection = {
            "timestamp": row[1],
            "user_id": row[2],
            "real_example_id": row[3],
            "synthetic_example_id": row[4],
            "selected_real": row[5],
            "model_id": row[6],
            "instruct_lang": row[7],
            "generation_method": row[8],
        }
        selections.append(selection)
    return selections


def admin_page():
    """Display the user selections from the database on the selections page."""
    st.title("View Selections")
    # Load and display user selections from the database
    st.write("User Selections")
    user_selections = load_selections_from_db()

    # Add a download button for all data
    all_data = pd.DataFrame(user_selections)
    csv = all_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download all data",
        data=csv,
        file_name="all_selections.csv",
        mime="text/csv",
    )
    if not user_selections:
        st.write("No selections found.")
        return

    if st.button("Show selections"):
        for idx, selection in enumerate(user_selections, 1):
            st.write(f"#### Selection {idx}")
            st.write(f'Timestamp: {selection["timestamp"]}')
            st.write(f'User ID: {selection["user_id"]}')
            st.write(f'Selected Real Example: {selection["selected_real"]}')
            st.write(f'Real Example ID: {selection["real_example_id"]}')
            st.write(f'Synthetic Example ID: {selection["synthetic_example_id"]}')
            st.write(f'Model ID: {selection["model_id"]}')
            st.write(f'Instruct Language: {selection["instruct_lang"]}')
            st.write(f'Generation Method: {selection["generation_method"]}')


if __name__ == "__main__":
    admin_page()
