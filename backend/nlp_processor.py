import spacy
import csv
import os
from database import Neo4jConnection

# Load English NLP Model
try:
	nlp = spacy.load("en_core_web_sm")
except OSError:
	print("Downloading spaCy model...")
	os.system("python3 -m spacy download en_core_web_sm")
	nlp = spacy.load("en_core_web_sm")

db = Neo4jConnection("bolt://localhost:7687", "neo4j", "nexus123") # Apna actual Neo4j password check kar lena

def process_firs():
	current_dir = os.path.dirname(os.path.abspath(__file__))
	data_file = os.path.join(os.path.dirname(current_dir), 'data', 'firs.csv')
	
	print("Starting NLP Analysis on FIRs...")
	with open(data_file, 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			fir_id = row['fir_id']
			text = row['text']
			
			# AI extracts entities from raw text
			doc = nlp(text)
			suspects = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
			
			for suspect in suspects:
				# Create FIR node and link to existing Person node
				query = """
				MATCH (p:Person {name: $name})
				MERGE (f:FIR {id: $fir_id, text: $text})
				MERGE (p)-[:SUSPECT_IN]->(f)
				"""
				db.query(query, parameters={"name": suspect, "fir_id": fir_id, "text": text})
				print(f"Linked FIR {fir_id} to Suspect: {suspect}")

	print("NLP Processing Complete.")
	db.close()

if __name__ == "__main__":
	process_firs()