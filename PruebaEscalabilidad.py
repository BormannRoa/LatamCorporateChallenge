from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    @task
    def get_data(self):
        self.client.get("/api/your-endpoint")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 9000
