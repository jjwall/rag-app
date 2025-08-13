import httpx
import ollama

def run_agent():
    inference = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])
    print(inference)

run_agent()

def get_data():
    url1 = "http://localhost:8001/send_data"
    url2 = "http://localhost:8001/receive_data"

    data = '''
    {
        "text": "This is test #2"
    }
    '''

    response = httpx.post(url1, data=data, headers={"Content-Type": "application/json"})
    # response = httpx.get(url2, headers={"Content-Type": "application/json"})
    # print(response.json())
    responseJson = response.json()
    print(responseJson) # ['data']['text'])
