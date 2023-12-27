import requests
import pprint


auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwNzI1ODA4LCJpYXQiOjE2OTA3MjUzNzEsImp0aSI6IjNmMWYwZmFhNjg0YjQyMGU5ODYxYTIwN2MyOGFmMzE2IiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJ0aW1vdGh5Y2h1biIsIm5hbWUiOiJcdWNjOWNcdWM5MDBcdWJiZmMifQ.fTRs0PXgBTf3kVOS5P3YFxaM35RxilHYCNDfAL-8Xq4"

year = 2021

baseURL = "http://127.0.0.1:8000/api/"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"}

response = requests.get(f"{baseURL}create_progress_cal/?year={year}", headers=headers)
print(response.status_code)
pprint.pprint(response.json())
