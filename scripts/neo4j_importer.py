import csv
import os
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "nexus123")  # Yahan apna Neo4j password dalna

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def run_query(tx, query, params=None):
	tx.run(query, params or {})

def import_to_db():
	driver = GraphDatabase.driver(URI, auth=AUTH)
	with driver.session() as session:
		# Puraana data clean kar do (agar kuch ho)
		session.execute_write(run_query, "MATCH (n) DETACH DELETE n")
		
		print("Uploading Persons...")
		with open(os.path.join(DATA_DIR, 'persons.csv'), 'r') as f:
			for row in csv.DictReader(f):
				q = "MERGE (p:Person {id: $id}) SET p.name = $name, p.address = $addr"
				session.execute_write(run_query, q, {"id": row['person_id'], "name": row['name'], "addr": row['address']})
		
		print("Uploading Phones & Links...")
		with open(os.path.join(DATA_DIR, 'phones.csv'), 'r') as f:
			for row in csv.DictReader(f):
				q = """
				MATCH (p:Person {id: $owner})
				MERGE (ph:Phone {number: $phone})
				MERGE (p)-[:OWNS]->(ph)
				"""
				session.execute_write(run_query, q, {"owner": row['owner_id'], "phone": row['phone_number']})
		
		print("Uploading Call Records (CDRs)...")
		with open(os.path.join(DATA_DIR, 'cdrs.csv'), 'r') as f:
			for row in csv.DictReader(f):
				q = """
				MATCH (c:Phone {number: $caller}), (r:Phone {number: $receiver})
				MERGE (c)-[:CALLED]->(r)
				"""
				session.execute_write(run_query, q, {"caller": row['caller_phone'], "receiver": row['receiver_phone']})
		
	driver.close()
	print("Database successfully populated! Graph is ready.")

if __name__ == "__main__":
	import_to_db()