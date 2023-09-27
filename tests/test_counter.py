"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

import json

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
    
    def test_update_a_counter(self):
        """It should update a counter"""
        name = "cntr"
        fqdn = "/counters/" + name
        result = self.client.post(fqdn)  # Create
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        baseline = result.get_json()[name]      # Result
        result = self.client.put(fqdn)  # Update
        self.assertEqual(result.status_code, status.HTTP_200_OK) # 200
        self.assertEqual(baseline+1, result.get_json()[name])             #

    def test_update_a_counter_fail(self):
        """It should return 404, update nonexist-counter"""
        result = self.client.put("/counters/IDontExist")  # Update
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_counter(self):
        """It should read the counter"""
        result = self.client.post("/counters/cnt")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.get("/counters/cnt")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(0, result.get_json()["cnt"])

    def test_get_a_counter_fail(self):
        """It should 404 when reading non-existent counter"""
        result = self.client.get("/counters/IDontExist")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
