import json
import azure.functions as func
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Cosmos DB configuration
    endpoint = "***********************"
    key = "***********************"
    database_name = "ToDoList"
    container_name = "Items"

 # Initialize Cosmos DB client
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

 # Query the database
    query = "SELECT c.Body FROM c"
    query_result = container.query_items(query, enable_cross_partition_query=True)

    # Extract relevant data from each item
    results = []
    for item in query_result:
        body = item.get('Body', {})
        #enqueued_time = item.get('iothub-enqueuedtime', '')
        result_item = {"Body": body}
        results.append(result_item)

    # Return the results in the desired format
    return func.HttpResponse(
        body=json.dumps(results, indent=2),  # Pretty print with indentation
        mimetype="application/json",
        status_code=200
    )