# 🕵️‍♂️ Nexus Squad Intelligence
**AI-Powered Criminal Network & Communications Radar**  
*Developed by Yugen Dynamics for Smart India Hackathon (SIH)*

![SIH](https://img.shields.io/badge/Smart_India_Hackathon-Ready-success?style=for-the-badge&logo=hackaday)
![Python](https://img.shields.io/badge/Python-FastAPI-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React.js-Cytoscape-61DAFB?style=for-the-badge&logo=react)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_DB-018bff?style=for-the-badge&logo=neo4j)

## 📌 Project Overview
Law enforcement agencies often struggle to connect the dots between scattered Call Detail Records (CDRs) and unstructured, text-heavy FIR reports. **Nexus Squad Intelligence** is an end-to-end AI platform that ingests raw communication logs and English FIR texts, processes them using Natural Language Processing (NLP), and maps the hidden connections into a highly interactive Graph Database. 

The system automatically calculates network centrality to identify the **Kingpin** (Gang Leader) of the syndicate, enabling precision strikes and intelligent law enforcement.

## 🚀 Key Features
- **🧠 AI Brain (NLP Processor):** Uses `spaCy` for Named Entity Recognition (NER) to automatically parse raw FIR text, extract suspect names, and link them to their respective criminal profiles.
- **🕸️ Interactive Cyber Graph:** Powered by `Cytoscape.js`, the dashboard renders suspects (Cyan Nodes) and AI-detected FIRs (Red Hexagons) with draggable, physics-based interactions.
- **🚨 Automated Kingpin Detection:** Implements graph algorithms (Centrality/Influence calculation) to automatically detect and alert authorities about the most influential nodes (leaders) in the network.
- **⚡ High-Performance API:** Built on `FastAPI` with automated interactive `Swagger UI` documentation for seamless frontend-backend communication.
- **🗄️ Graph Database Integration:** Uses `Neo4j` to accurately map complex hierarchical relationships, `OWNS` connections, and `CALLED` edges.

## 🛠️ Tech Stack
- **Frontend:** React.js, Cytoscape.js, Axios, CSS (Dark Cyberpunk Theme)
- **Backend:** Python 3, FastAPI, Uvicorn, spaCy (NLP), Pydantic
- **Database:** Neo4j (Cypher Query Language)

## ⚙️ Installation & Setup

### 1. Database Setup (Neo4j)
Ensure Neo4j is installed and running on your system (Port `7474`/`7687`).
```bash
	sudo systemctl start neo4j
