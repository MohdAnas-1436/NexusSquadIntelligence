from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Neo4jConnection
import graph_algorithms
from models import KingpinResponse, MiddlemanResponse

app = FastAPI(title="Criminal Network Intel API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"], 
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Update "nexus123" with your actual Neo4j password if different
db = Neo4jConnection("bolt://localhost:7687", "neo4j", "nexus123")

@app.get("/")
def read_root():
	return {"Status": "Intelligence Server is Running"}

@app.get("/api/kingpin", response_model=KingpinResponse)
def find_kingpin():
	result = graph_algorithms.get_kingpin(db)
	if not result:
		return {"top_suspects": []}
	
	kingpins = [{"id": record["ID"], "name": record["Name"], "score": record["InfluenceScore"]} for record in result]
	return {"top_suspects": kingpins}

@app.get("/api/middlemen", response_model=MiddlemanResponse)
def find_middlemen():
	result = graph_algorithms.get_middlemen(db)
	if not result:
		return {"middlemen": []}
	
	middlemen = [{"id": record["ID"], "name": record["Name"], "connections": record["UniqueConnections"]} for record in result]
	return {"middlemen": middlemen}

@app.get("/api/network")
def get_full_network():
	query = """
	MATCH (p1:Person)-[:OWNS]->(ph1:Phone)-[c:CALLED]->(ph2:Phone)<-[:OWNS]-(p2:Person)
	RETURN p1.id AS source_id, p1.name AS source_name, 'Person' AS source_type,
	       p2.id AS target_id, p2.name AS target_name, 'Person' AS target_type,
	       'CALLED' AS edge_label
	UNION
	MATCH (p:Person)-[:SUSPECT_IN]->(f:FIR)
	RETURN p.id AS source_id, p.name AS source_name, 'Person' AS source_type,
	       f.id AS target_id, f.id AS target_name, 'FIR' AS target_type,
	       'SUSPECT_IN' AS edge_label
	"""
	results = db.query(query)
	
	nodes = {}
	edges = []
	
	for row in results:
		src_id = row["source_id"]
		tgt_id = row["target_id"]
		
		if src_id not in nodes:
			nodes[src_id] = {"data": {"id": src_id, "label": row["source_name"], "type": row["source_type"]}}
		if tgt_id not in nodes:
			nodes[tgt_id] = {"data": {"id": tgt_id, "label": row["target_name"], "type": row["target_type"]}}
			
		edges.append({"data": {"source": src_id, "target": tgt_id, "label": row["edge_label"]}})
	
	return {"elements": list(nodes.values()) + edges}

@app.on_event("shutdown")
def shutdown_event():
	db.close()