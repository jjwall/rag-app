import requests
import json

# Test cases for the interview
TEST_CASES = [
    {
        "name": "High Priority - System Down",
        "expected_priority": 1,
        "payload": {
            "title": "Production system completely offline",
            "description": "All users unable to access main application. Database connection errors across all servers. Complete service outage.",
            "user_type": "enterprise",
            "affected_systems": ["core", "database", "api"],
        },
    },
    {
        "name": "Medium Priority - Premium User Login",
        "expected_priority": 2,
        "payload": {
            "title": "Can't access my account",
            "description": "I've been locked out since yesterday after trying to reset my password. Premium customer needs urgent access.",
            "user_type": "premium",
            "affected_systems": ["login", "dashboard"],
        },
    },
    {
        "name": "Low Priority - Standard Password Reset",
        "expected_priority": 4,
        "payload": {
            "title": "Password reset help",
            "description": "I forgot my password and need help resetting it. Not urgent, just when someone has time.",
            "user_type": "standard",
            "affected_systems": ["login"],
        },
    },
    {
        "name": "Medium Priority - Billing Issue",
        "expected_priority": 3,
        "payload": {
            "title": "Billing discrepancy on invoice",
            "description": "My latest invoice shows charges for features I never activated. Need this resolved before next billing cycle.",
            "user_type": "premium",
            "affected_systems": ["billing"],
        },
    },
    {
        "name": "High Priority - Security Concern",
        "expected_priority": 1,
        "payload": {
            "title": "Suspicious account activity",
            "description": "Multiple failed login attempts from foreign IP addresses. Concerned about potential security breach.",
            "user_type": "enterprise",
            "affected_systems": ["login", "security"],
        },
    },
    {
        "name": "Low Priority - Feature Request",
        "expected_priority": 5,
        "payload": {
            "title": "Export to Excel feature",
            "description": "Would be nice to have Excel export instead of just CSV. Not urgent, just a nice-to-have feature.",
            "user_type": "standard",
            "affected_systems": ["reports"],
        },
    },
]


def test_classify_endpoint(base_url="http://localhost:8000"):
    """Test the classify endpoint with sample cases"""

    print("🧪 Testing AI Ticket Classifier\n")

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Expected Priority: {test_case['expected_priority']}")

        try:
            response = requests.post(
                f"{base_url}/classify", json=test_case["payload"], timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                actual_priority = result.get("priority")
                reasoning = result.get("reasoning", "")
                confidence = result.get("confidence", 0)

                print(f"✅ Actual Priority: {actual_priority}")
                print(f"📝 Reasoning: {reasoning}")
                print(f"🎯 Confidence: {confidence:.2f}")

                # Simple accuracy check
                if abs(actual_priority - test_case["expected_priority"]) <= 1:
                    print("✅ PASS - Priority within acceptable range")
                else:
                    print("❌ FAIL - Priority outside expected range")

            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

        print("-" * 50)


def test_health_endpoint(base_url="http://localhost:8000"):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except:
        print("❌ Cannot connect to API")
        return False


if __name__ == "__main__":
    # Test health first
    if test_health_endpoint():
        test_classify_endpoint()
    else:
        print("🚨 API not accessible. Make sure Docker containers are running:")
        print("   docker-compose up -d")
        print("   python populate_chroma_db.py")
