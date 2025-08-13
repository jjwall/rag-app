import chromadb
import json
import os
import time

# Sample historical tickets for ChromaDB
SAMPLE_TICKETS = [
    {
        "id": "ticket_001",
        "document": "Production database is completely down. All users unable to access the application. Critical system failure affecting entire customer base.",
        "metadata": {
            "priority": 1,
            "category": "technical",
            "resolution_time_hours": 2,
            "user_type": "enterprise",
            "resolved": True,
        },
    },
    {
        "id": "ticket_002",
        "document": "User unable to login to their account. Password reset not working. Premium customer locked out since yesterday.",
        "metadata": {
            "priority": 2,
            "category": "login",
            "resolution_time_hours": 4,
            "user_type": "premium",
            "resolved": True,
        },
    },
    {
        "id": "ticket_003",
        "document": "Need help resetting my password. Forgot credentials and can't access the reset email.",
        "metadata": {
            "priority": 4,
            "category": "login",
            "resolution_time_hours": 1,
            "user_type": "standard",
            "resolved": True,
        },
    },
    {
        "id": "ticket_004",
        "document": "Billing invoice shows incorrect charges. Overcharged for premium features not used.",
        "metadata": {
            "priority": 3,
            "category": "billing",
            "resolution_time_hours": 24,
            "user_type": "premium",
            "resolved": True,
        },
    },
    {
        "id": "ticket_005",
        "document": "Application is running very slowly. Page load times over 30 seconds. Performance degradation affecting workflow.",
        "metadata": {
            "priority": 2,
            "category": "performance",
            "resolution_time_hours": 8,
            "user_type": "enterprise",
            "resolved": True,
        },
    },
    {
        "id": "ticket_006",
        "document": "Cannot access admin dashboard. Getting 500 error when trying to view user management section.",
        "metadata": {
            "priority": 2,
            "category": "access",
            "resolution_time_hours": 6,
            "user_type": "enterprise",
            "resolved": True,
        },
    },
    {
        "id": "ticket_007",
        "document": "Feature request: Would like to export data to Excel format. Current CSV export is insufficient.",
        "metadata": {
            "priority": 5,
            "category": "technical",
            "resolution_time_hours": 72,
            "user_type": "standard",
            "resolved": False,
        },
    },
    {
        "id": "ticket_008",
        "document": "Security concern: Suspicious login attempts from unknown IP addresses. Need to investigate potential breach.",
        "metadata": {
            "priority": 1,
            "category": "access",
            "resolution_time_hours": 1,
            "user_type": "enterprise",
            "resolved": True,
        },
    },
    {
        "id": "ticket_009",
        "document": "Mobile app crashes when trying to upload large files. Affects premium users with high-resolution images.",
        "metadata": {
            "priority": 3,
            "category": "technical",
            "resolution_time_hours": 16,
            "user_type": "premium",
            "resolved": True,
        },
    },
    {
        "id": "ticket_010",
        "document": "Question about billing cycle. When will next invoice be generated and what payment methods are accepted?",
        "metadata": {
            "priority": 4,
            "category": "billing",
            "resolution_time_hours": 2,
            "user_type": "standard",
            "resolved": True,
        },
    },
]


def populate_chromadb():
    """Populate ChromaDB with sample historical tickets"""

    # Connect to ChromaDB
    client = chromadb.HttpClient(host="localhost", port=8001)

    # Delete collection if it exists (for clean setup)
    try:
        client.delete_collection("historical_tickets")
    except:
        pass

    # Create collection
    collection = client.create_collection("historical_tickets")

    # Extract data for ChromaDB
    documents = [ticket["document"] for ticket in SAMPLE_TICKETS]
    metadatas = [ticket["metadata"] for ticket in SAMPLE_TICKETS]
    ids = [ticket["id"] for ticket in SAMPLE_TICKETS]

    # Add to collection
    collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print(
        f"✅ Successfully populated ChromaDB with {len(SAMPLE_TICKETS)} historical tickets"
    )

    # Test query
    results = collection.query(query_texts=["login problems"], n_results=3)

    print(f"🔍 Test query returned {len(results['documents'][0])} similar tickets")
    for i, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        print(f"  - Priority {metadata['priority']}: {doc[:50]}...")


if __name__ == "__main__":
    populate_chromadb()
