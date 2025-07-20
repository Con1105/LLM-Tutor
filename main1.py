from streamlit.web import cli as stcli
import sys
from kg_instance import get_kg

if __name__ == "__main__":
    # Initialize KGGen here in the true main thread
    print("Initializing KGGen in main thread...")
    kg = get_kg()  # this is now safe

    # Replace sys.argv so Streamlit thinks it was launched from CLI
    sys.argv = ["streamlit", "run", "kg_ui.py"]
    sys.exit(stcli.main())
