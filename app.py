import streamlit as st

st.set_page_config(layout="wide", page_title="Reale vs Synthetische Konversationen", page_icon="🤖")

st.title("Reale vs Synthetische Konversationen")

st.subheader("Experimentelle Untersuchung")

st.write(
    """
    Willkommen zu unserem Experiment zur Unterscheidung zwischen realen und synthetischen Konversationen.\n
    In diesem Experiment werden Ihnen paarweise zwei verschiedene Konversationsskripte angezeigt.\n
    Eine der Konversationen wurde von einer KI generiert, während die andere Konversation von einer realen Person geführt wurde.\n
    Ihre Aufgabe ist es, zu beurteilen, welches der beiden Skripte Sie als die eche Konversation einschätzen.\n
    Informationen wie Personennamen, Firmennamen und spezifische Details wurden in synthetischen und realen Daten anonymisiert.\n

    **Vorgehensweise:**
    1. Lesen Sie beide Konversationsskripte aufmerksam durch.
    2. Entscheiden Sie, welches Skript Sie für die echte Konversation halten.
    3. Bestätigen Sie Ihre Auswahl durch Drücken des Knopfes "Auswahl bestätigen".
    4. Nach jeder Auswahl werden Ihnen zwei neue Konversationsskripte angezeigt.
    5. Nachdem Sie 10 Entscheidungen getroffen haben, werden Sie automatisch weitergeleitet.

    Ihre Teilnahme an diesem Experiment hilft uns, die Unterscheidung zwischen realen und synthetischen Texten zu verbessern.\n
    Vielen Dank für Ihre Unterstützung!
    """
)

if st.button("Zum Experiment"):
    st.switch_page("pages/1_experiment.py")
