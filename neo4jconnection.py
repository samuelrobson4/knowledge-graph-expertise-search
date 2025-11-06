from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

# Test connection
with driver.session() as session:
    result = session.run("RETURN 'Connected!' as message")
    print(result.single()["message"])

driver.close()