from pydantic import BaseModel
from typing import List, Optional

# Kingpin API Response Model
class KingpinModel(BaseModel):
	id: str
	name: str
	score: int

class KingpinResponse(BaseModel):
	top_suspects: List[KingpinModel]

# Middlemen API Response Model
class MiddlemanModel(BaseModel):
	id: str
	name: str
	connections: int

class MiddlemanResponse(BaseModel):
	middlemen: List[MiddlemanModel]

# Future Scope: Agar humein frontend se naya FIR ya suspect manually add karna ho
class SuspectCreate(BaseModel):
	name: str
	phone_number: str
	address: str

class FIRCreate(BaseModel):
	fir_id: str
	date: str
	text: str