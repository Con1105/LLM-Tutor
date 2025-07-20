from streamlit.web import cli as stcli
import sys
from kg_gen import KGGen  # or wherever KGGen is defined


kg = None

def get_kg():
    if kg is None:
        raise RuntimeError("KGGen must be initialized in main1.py before use.")
    return kg

if __name__ == "__main__":
    # Initialize KGGen here in the true main thread
    print("Initializing KGGen in main thread...")
    print("✅ Initializing KGGen in main thread...")
    kg = KGGen(
        model="openai/gpt-4o",
        temperature=0.0,
        api_key="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"
    )

    # Replace sys.argv so Streamlit thinks it was launched from CLI
    sys.argv = ["streamlit", "run", "kg_ui.py"]
    sys.exit(stcli.main())
