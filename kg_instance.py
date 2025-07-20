# kg_instance.py
kg = None

def set_kg_instance(instance):
    global kg
    kg = instance

def get_kg_instance():
    if kg is None:
        raise RuntimeError("KGGen instance is not initialized. Make sure main.py ran first.")
    return kg
