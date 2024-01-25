from locust import HttpUser, task, between
import requests

class ServerTest(HttpUser):
    host = "https://user01.ssgeco.store"
    token = None

    def on_start(self):
        # 로그인하여 토큰 획득
        response = self.client.post(
            "/login",
            json={"email": "test@test.com", "password": "testtest"}
        )
        self.token = response.json().get("token")

    @task
    def login_and_get_token(self):
        # 로그인 태스크는 첫 번째로 실행
        response = self.client.post(
            "/login",
            json={"email": "test@test.com", "password": "testtest"}
        )
        self.token = response.json().get("token")
        
    @task
    def test_image_endpoint(self):
        # 이미지 업로드 태스크는 두 번째로 실행
        if self.token is not None:
            image_path = "test.jpg"  # Set the path to your test image
            print(f"Image Path: {image_path}")

            try:
                with open(image_path, "rb") as file:
                    files = {'image': ('test.jpg', file, 'image/jpeg')}
                    headers = {'x-access-token': self.token}  # Use the actual access token
                    response = self.client.post('/image', files=files, headers=headers)

                    # Check the response status
                    if response.ok:
                        print("Image upload successful")
                    else:
                        print("Image upload failed")
                        print(f"Status Code: {response.status_code}")
                        print("Response Content:", response.text)

            except FileNotFoundError:
                print(f"Error: File not found at path '{image_path}'")
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP Error: {http_err}")
            except requests.exceptions.ChunkedEncodingError as chunked_err:
                print(f"Chunked Encoding Error: {chunked_err}")
            except requests.exceptions.RequestException as req_err:
                print(f"Request Exception: {req_err}")
        else:
            print("Error: Access token is not available. Please provide a valid access token.")

    wait_time = between(5,20)  # 각 태스크 사이의 대기 시간 (초 단위)을 지정
