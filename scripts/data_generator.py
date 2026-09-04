import csv
import random
import os
from datetime import datetime, timedelta

# Auto-detect data folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

FIRST_NAMES = ["Rahul", "Amit", "Priya", "Neha", "Vikram", "Suresh", "Ramesh", "Sunita", "Anjali", "Karan"]
LAST_NAMES = ["Sharma", "Singh", "Verma", "Kumar", "Gupta", "Yadav", "Mishra", "Patel", "Das", "Jain"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"]

NUM_PERSONS = 30
NUM_CDRS = 200

def generate_data():
	persons = []
	phones = []
	
	print("Generating synthetic criminals...")
	for i in range(1, NUM_PERSONS + 1):
		pid = f"P{i:03}"
		name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
		persons.append([pid, name, random.randint(20, 65), random.choice(CITIES)])
		phones.append([f"+91-{random.randint(6000000000, 9999999999)}", pid])

	cdrs = []
	start_date = datetime.now() - timedelta(days=30)
	kingpin, mid1, mid2 = phones[0][0], phones[1][0], phones[2][0]

	print("Generating communication network (CDRs)...")
	for _ in range(NUM_CDRS):
		rand_val = random.random()
		if rand_val < 0.3: caller, receiver = mid1, random.choice(phones[3:15])[0]
		elif rand_val < 0.6: caller, receiver = mid2, random.choice(phones[15:])[0]
		elif rand_val < 0.8: caller, receiver = kingpin, random.choice([mid1, mid2])
		else: caller, receiver = random.choice(phones)[0], random.choice(phones)[0]
		
		while caller == receiver: receiver = random.choice(phones)[0]
		time_str = (start_date + timedelta(minutes=random.randint(0, 43200))).strftime("%Y-%m-%d %H:%M:%S")
		cdrs.append([caller, receiver, time_str, random.randint(10, 3600), random.choice(CITIES)])

	firs = []
	for i in range(1, 11):
		suspect = random.choice(persons)
		firs.append([f"FIR{i:03}", "2026-08-15", f"Suspicious activity at {random.choice(CITIES)}. Main suspect is {suspect[1]}."])

	# Write to CSV
	def write_csv(name, headers, data):
		with open(os.path.join(DATA_DIR, name), 'w', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(headers)
			writer.writerows(data)

	write_csv('persons.csv', ['person_id', 'name', 'age', 'address'], persons)
	write_csv('phones.csv', ['phone_number', 'owner_id'], phones)
	write_csv('cdrs.csv', ['caller_phone', 'receiver_phone', 'timestamp', 'duration', 'tower_location'], cdrs)
	write_csv('firs.csv', ['fir_id', 'date', 'text'], firs)
	print("Data successfully generated in 'data' folder!")

if __name__ == "__main__":
	generate_data()