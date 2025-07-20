# kg_instance.py
# Global variables to hold instance and initializing thread ID
kg = None
kg_thread_id = None

def set_kg_instance(instance):
    global kg
    kg = instance

def get_kg_instance():
    if kg is None:
        raise RuntimeError("KGGen instance is not initialized. Make sure main.py ran first.")
    return kg
