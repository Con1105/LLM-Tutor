# Intelligent Tutor System Prototypes

This repository contains two prototype applications developed as part of a dissertation project on LLM-based Intelligent Tutoring System (ITS) for Academic Papers. Both applications are implemented in **Streamlit** and deployed on the Streamlit Community Cloud.

---

## 📘 1. Content Model Module Tool

- **Interface:** `kg_ui.py`  
- **Core logic:** `kg_extraction.py`  
- **NER filtering:** `ner_filtering.py`  

The **Content Model Module Tool** allows a user to upload an academic paper through a Streamlit interface (`kg_ui.py`). The interface passes the PDF to the backend (`kg_extraction.py`), which creates a **knowledge graph (KG)** of concepts and their prerequisite relationships.  

As part of the extraction pipeline, the tool calls **spaCy** (via `ner_filtering.py`) to perform Named Entity Recognition (NER) and tag nodes in the graph.
🔗 Live app: [Content Model Module Tool](https://llm-tutor-int5fhkcsicwhsgq2pfu3s.streamlit.app/)

---

## 🎓 2. Tutoring Tool

- **Interface:** `text_input_page.py`  
- **LLM Agents:**  
  - `tutor.py` (interactive tutoring agent)  
  - `evaluator_agent.py` (quiz generation and assessment)  

The **Tutoring Tool** provides an interactive learning interface. Users can enter a concept of their choice, receive a **reading-style lesson** from the tutoring agent, and then engage in a Q/A session. Once ready, the user can trigger the evaluator agent, which generates a quiz aligned with the lesson and interaction.  

The Streamlit interface (`text_input_page.py`) coordinates the flow between user input, the tutor agent (`tutor.py`), and the evaluator agent (`evaluator_agent.py`). Together, these components simulate an ITS session with short-term teaching, interaction, and assessment.

🔗 Live app: [Tutoring Tool](https://llm-tutor-ifurra8fgsx5ttyfrcem62.streamlit.app/)

---

## ⚙️ Data and LLM Calls

- **No datasets were used** for this project.  
- Instead, both applications rely on **calls to large language models (LLMs)** through the **ELM API key provided by the University of Edinburgh**.  
- The API key itself is **not revealed in the code** for security reasons.

---

## 📦 Requirements

All necessary dependencies are listed in `requirements.txt`. Install them via:

```bash
pip install -r requirements.txt

```
## 📂 Repository

The full source code is available here: [LLM-Tutor on GitHub](https://github.com/Con1105/LLM-Tutor)
