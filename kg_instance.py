# kg_instance.py
# Global variables to hold instance and initializing thread ID
kg = None
kg_thread_id = None

def set_kg_instance(instance):
    global kg
    kg = instance

def set_thread_instance(instance):
    global kg_thread_id
    kg_thread_id = instance

def get_kg_instance():
    if kg is None:
        raise RuntimeError("KGGen instance is not initialized. Make sure main.py ran first.")
    current_id = threading.get_ident()
    if current_id != kg_thread_id:
        raise RuntimeError(
            f"KGGen can only be used from the thread where it was initialized "
            f"(thread ID: {kg_thread_id}), but this call came from thread ID: {current_id}."
        )
    return kg
