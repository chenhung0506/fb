from locust import HttpUser, TaskSet, task


class WebsiteTasks(TaskSet):
    @task(1)
    def index(self):
        self.client.get('/')


class WebsiteUser(HttpUser):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000

    #  locust -f locustfile.py -H http://192.168.2.69:5000 --no-web -c 100 -r 10 -t 600s