import threading
from kg_gen import KGGen

_kg_instance = None  # private singleton instance

def get_kg():
    global _kg_instance

    if _kg_instance is None:
        # Ensure this runs in the main thread
        if threading.current_thread() != threading.main_thread():
            raise RuntimeError("KGGen() must be initialized in the main thread.")

        print("[INFO] Initializing KGGen in main thread...")
        _kg_instance = KGGen(
            model="openai/gpt-4o",
            temperature=0.0,
            api_key="your-api-key"  # <- Replace this with `st.secrets` or env variable
        )
        print("[INFO] KGGen initialized.")

    return _kg_instance
