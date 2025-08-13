import httpx
import ollama
import json
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

local_model = 'llama3.2'
embedding_model = 'nomic-embed-text'

def load_vector_db():
    data_to_load = ["The sky is yellow."]
    vector_db = Chroma.from_texts(data_to_load, OllamaEmbeddings(model=embedding_model))
    retriever = vector_db.as_retriever()
    question = "What color is the sky?"
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs) # docs.page_content
    print(context)

    formatted_prompt = f"""Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """
    formatted_prompt += """
    Respond only with valid JSON in the format of: 

    {
        "answer": [your response goes here]
    }
    
    . Do not write an introduction or summary.
    """

    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': formatted_prompt}])
    response_content = response['message']['content']
    response_content_dict = json.loads(response_content)
    print(response_content_dict["answer"])

load_vector_db()


def run_agent():
    inference = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])
    print(inference)

# run_agent()

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
