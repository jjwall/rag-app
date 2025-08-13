import httpx

url = "http://localhost:8001/send_data"

data = '''
{
    "text": "This is test #2"
}
'''

response = httpx.post(url, data=data, headers={"Content-Type": "application/json"})
# print(response.json())
responseJson = response.json()
print(responseJson['data_sent'])
