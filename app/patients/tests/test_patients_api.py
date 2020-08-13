from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from app.core.models import Patient

from app.patients.serializers import PatientSerializer

PATIENTS_URL = reverse('patients')


class PublicPatientsApiTests(TestCase):
    """Test the publicity available patients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving patients"""
        res = self.client.get(PATIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePatientsApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'Test123'
        )

        self.client = APIClient(        )
        self.client.force_authenticate(self.user)

    def test_retrive_patients(self):
        """Test retrieving patients"""
        Patient.objects.create(doctor=self.user, name='Jan', surname='Kowalski')
        Patient.objects.create(doctor=self.user, name='Janek', surname='Kowalski')

        res = self.client.get(PATIENTS_URL)

        patients = Patient.objects.all().order_by('-surname')
        serializer = PatientSerializer(patients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patients_limited_to_doctor(self):
        """Test that patients returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'Test123'
        )
        Patient.objects.create(user=user2, name='Anna', surname='Kowalska')
        patient = Patient.objects.create(doctor=self.user, name='Joanna', surname='Kowalska')

        res = self.client.get(PATIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], patient.name)