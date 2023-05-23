from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from modern_programming_technologies.api.api.models import RepairJob


class RepairJobAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.repair_job = {
            "car_make": "Toyota",
            "car_model": "Camry",
            "description": "Замена масла и фильтра",
            "price": 100
        }

    def test_list_repair_jobs(self):
        url = reverse('apis-repairjob-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_repair_job(self):
        url = reverse('apis-repairjob-list')
        response = self.client.post(url, data=self.repair_job)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_repair_job(self):
        job_id = RepairJob.objects.first().id
        url = reverse('apis-repairjob-detail', args=[job_id])
        update_data = {"price": 120}
        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_repair_job(self):
        job_id = RepairJob.objects.first().id
        url = reverse('apis-repairjob-detail', args=[job_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)