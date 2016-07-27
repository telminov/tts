from rest_framework.test import APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from django.conf import settings

import os
import json
import shutil


class TestGenerateView(APITestCase):
    url = reverse('Core:generate')

    def test_generate(self):
        response = self.client.post(self.url, {'text': 'Awesome Text!'})
        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['status'], 0)
        self.assertTrue(os.path.exists('%s/%s.wav' % (settings.OUTPUT_DIR, content['uuid'])))

    def tearDown(self):
        shutil.rmtree(settings.OUTPUT_DIR)


class TestGetFileView(APITestCase):
    get_url = reverse('Core:get_file')
    gen_url = reverse('Core:generate')

    def test_get_file(self):
        gen_response = self.client.post(self.gen_url, {'text': 'Awesome Text!'})
        gen_content = json.loads(gen_response.content.decode('utf-8'))

        get_response = self.client.get(self.get_url, {'uuid': gen_content['uuid']})

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response['Content-Disposition'], 'attachment; filename=%s.wav' % gen_content['uuid'])
        # TODO Пока неясно, как проверить наличие файла в response'е
