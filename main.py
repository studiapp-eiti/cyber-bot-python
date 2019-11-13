from studia3.studia_requests import Studia3Client
username = None
password = None

if __name__ =="__main__":
    client = Studia3Client()
    client.log_in(username, password)
