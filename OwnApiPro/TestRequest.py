import requests

def send_request():
    data = {"question": "ile mam samochodów?"}
    #data = {"question": "Jaki jest mój ulubiony kolor?"}
    response = requests.post("http://localhost:5000/ownapi_1", json=data) 
    #response = requests.post("https://apijest.toadres.pl/ownapi_1", json=data)
    if response.status_code == 200:
        print("Response from server:", response.json())
    else:
        print("Failed to get a response from the server")

if __name__ == "__main__":
    send_request()