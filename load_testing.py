from locust import HttpLocust, TaskSet

def get_location_JSON(l):
    h = {'Accept': 'application/JSON'}
    l.client.get('/api/v1/locations/696', headers=h)

def get_location_XML(l):
    h = {'Accept': 'text/xml'}
    l.client.get('/api/v1/locations/696', headers=h)


def get_locations_JSON(l):
    h = {'Accept': 'application/JSON'}
    l.client.get('/api/v1/locations', headers=h)

def get_locations_XML(l):
    h = {'Accept': 'text/xml'}
    l.client.get('/api/v1/locations', headers=h)


class UserBehavior(TaskSet):
    tasks = {
        get_location_JSON: 1,
        get_location_XML: 1,
        get_locations_JSON:1,
        get_locations_XML:1
    }


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 10000
