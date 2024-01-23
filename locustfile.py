from locust import HttpUser, task, between

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
    def test_profile_endpoint(self):
        # 프로필 정보 가져오기 태스크
        if self.token is not None:
            headers = {'x-access-token': self.token}
            response = self.client.get('/mypage', headers=headers)

            # Check the response status
            if response.ok:
                user_info = response.json()
                print(f"Profile fetched successfully: {user_info}")
            else:
                print("Failed to fetch profile information")

    # @task
    # def test_image_endpoint(self):
    #     # 이미지 업로드 태스크는 두 번째로 실행
    #     if self.token is not None:
    #         image_path = "test.jpg"  # Set the path to your test image
    #         with open(image_path, "rb") as file:
    #             files = {'image': ('test.jpg', file, 'image/jpeg')}
    #             headers = {'x-access-token': 'your_access_token'}  # Replace with the actual access token
    #             response = self.client.post('/image', files=files, headers=headers)

    #             # Check the response status
    #             if response.ok:
    #                 print("Image upload successful")
    #             else:
    #                 print("Image upload failed")

    wait_time = between(5, 10)  # 각 태스크 사이의 대기 시간 (초 단위)을 지정
