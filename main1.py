# from streamlit.web import cli as stcli
# import sys
# from kg_gen import KGGen
# from kg_instance import set_kg_instance, set_thread_instance
# import threading
# # import dspy
# # from dspy import OpenAI
# lock = threading.Lock()
# if __name__ == "__main__":
#     # Initialize KGGen here in the true main thread
#     with lock:
#         print("Initializing KGGen in main thread...")
#         print("✅ Initializing KGGen in main thread...")
#         set_thread_instance(threading.current_thread())
#         kg = KGGen(
#             model="openai/gpt-4o",
#             temperature=0.0,
#             api_key="OPENAI_API_KEY"
#         )
#         set_kg_instance(kg)
#     # Replace sys.argv so Streamlit thinks it was launched from CLI
#     sys.argv = ["streamlit", "run", "kg_ui.py"]
#     sys.exit(stcli.main())
