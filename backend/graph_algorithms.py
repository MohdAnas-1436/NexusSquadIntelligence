def get_kingpin(db_conn):
	# Cypher query to find the most influential node (Kingpin)
	query = """
	MATCH (p:Person)-[:OWNS]->(ph:Phone)-[c:CALLED]-(other:Phone)
	RETURN p.name AS Name, p.id AS ID, count(c) AS InfluenceScore
	ORDER BY InfluenceScore DESC
	LIMIT 5
	"""
	return db_conn.query(query)

def get_middlemen(db_conn):
	# Identifying potential middlemen based on unique connections
	query = """
	MATCH (p:Person)-[:OWNS]->(ph:Phone)
	MATCH (ph)-[:CALLED]-(other:Phone)
	WITH p, count(DISTINCT other) AS UniqueConnections
	RETURN p.name AS Name, p.id AS ID, UniqueConnections
	ORDER BY UniqueConnections DESC
	LIMIT 5
	"""
	return db_conn.query(query)