from locust import HttpUser, task, between


class GatewayUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def health_check(self):
        self.client.get("/api/v1/health")

    @task(2)
    def ping_check(self):
        self.client.get("/ping")

    @task(1)
    def login_and_profile(self):
        response = self.client.post("/login", json={"username": "admin", "password": "admin123"})
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            self.client.get("/profile", headers=headers)
