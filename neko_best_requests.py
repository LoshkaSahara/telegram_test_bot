import requests

DEFAULT_ADDRESS = "https://nekos.best/api/v2"
HEADERS = {'user-agent': 'my-app/0.0.1'}

def session_open():
    session = requests.Session()
    return session

def session_close(session):
    session.close
    
def get_querry(session, endpoint):
    response = session.get(f"{DEFAULT_ADDRESS}{endpoint}", headers=HEADERS)
    return response

def main():
    session = session_open()
    get_response = get_querry(session,"/endpoints")
    print(get_response.text)
    session_close(session)
    
if __name__ == "__main__":
    main()