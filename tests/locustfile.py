from locust import HttpLocust, TaskSet, task


class LocationsDetectTaskSet(TaskSet):

    @task
    def get(self):
        fp = open('./tests/example.csv', 'rb')
        self.client.post('/v1/import/', files={'file': fp})


class WebsiteUser(HttpLocust):
    task_set = LocationsDetectTaskSet
    min_wait = 100
    max_wait = 100
