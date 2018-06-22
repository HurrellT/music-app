import json
import unittest
from collections import namedtuple

import requests


class TrackTestCase(unittest.TestCase):

    def test_addTrack_Tema1_by_JoseYYY(self):
        jsonData = {'name': 'Jose',
                    'lastName': 'Perez',
                    'userName': 'JoseYYY',
                    'password': 'Clave1234._5'}
        addUserReq = requests.put('http://localhost:8080/apiv1/users', json=jsonData)

        putData = {'trackName': 'Tema 1', 'fileContent': 'contenido', 'owner': 'JoseYYY'}
        addTrackReq = requests.put('http://localhost:8080/apiv1/tracks', json=putData)

        self.assertEqual(200,addTrackReq .status_code)
        self.assertEqual('OK',addTrackReq .reason)
        self.assertEqual('Track added',addTrackReq .text)

    def test_get_existent_track_by_id(self):
        jsonData = {'name': 'Jose',
                    'lastName': 'Perez',
                    'userName': 'JoseYYY',
                    'password': 'Clave1234._5'}
        addUserReq = requests.put('http://localhost:8080/apiv1/users', json=jsonData)

        postData = {'trackName': 'Tema 1', 'fileContent': 'contenido', 'owner': 'JoseYYY'}
        addTrackReq = requests.put('http://localhost:8080/apiv1/tracks', json=postData)

        getTrackReq = requests.get('http://localhost:8080/apiv1/tracks/Tema 1')

        self.assertEqual(getTrackReq.status_code, 200)
        self.assertEqual(getTrackReq.reason, 'OK')
        jsonResponse = json.loads(getTrackReq.text)
        self.assertTrue(len(jsonResponse),1)

    def test_get_Nonexistent_track_by_id(self):
        getTrackReq = requests.get('http://localhost:8080/apiv1/tracks/Tema 2')
        self.assertEqual(getTrackReq.status_code, 200)
        self.assertEqual(getTrackReq.reason, 'OK')
        self.assertTrue(getTrackReq.content, 'No id was found')

    def test_get_two_tracks_with_substring_Tema(self):
        jsonData = {'name': 'Jose',
                    'lastName': 'Perez',
                    'userName': 'JoseYYY',
                    'password': 'Clave1234._5'}
        addUserReq = requests.put('http://localhost:8080/apiv1/users', json=jsonData)

        putData = {'trackName': 'Tema 1', 'fileContent': 'contenido', 'owner': 'JoseYYY'}
        addTrackReq = requests.put('http://localhost:8080/apiv1/tracks', json=putData)

        putData2 = {'trackName': 'Tema 2', 'fileContent': 'contenido2', 'owner': 'JoseYYY'}
        addTrackReq2 = requests.put('http://localhost:8080/apiv1/tracks', json=putData2)

        putData3 = {'trackName': 'Musica 1', 'fileContent': 'contenido3', 'owner': 'JoseYYY'}
        addTrackReq3 = requests.put('http://localhost:8080/apiv1/tracks', json=putData3)

        searchData = {'trackLikeName': 'Tema'}
        searchReq = requests.get('http://localhost:8080/apiv1/tracks',data = searchData)

        self.assertEqual(searchReq.status_code, 200)
        self.assertEqual(searchReq.reason, 'OK')
        jsonResponse = json.loads(searchReq.text)
        self.assertEqual(len(jsonResponse), 2)

        requests.delete('http://localhost:8080/apiv1/tracks/Tema 2')
        requests.delete('http://localhost:8080/apiv1/tracks/Musica 1')

    def test_updateTrackWithNameTema1(self):
        jsonData = {'name': 'Jose',
                    'lastName': 'Perez',
                    'userName': 'JoseYYY',
                    'password': 'Clave1234._5'}
        addUserReq = requests.put('http://localhost:8080/apiv1/users', json=jsonData)

        putData = {'trackName': 'Tema 1', 'fileContent': 'contenido', 'owner': 'JoseYYY'}
        addTrackReq = requests.put('http://localhost:8080/apiv1/tracks', json=putData)

        getTrackReq = requests.get('http://localhost:8080/apiv1/tracks/Tema 1')

        trackResponse = json.loads(getTrackReq.text, object_hook=lambda d: namedtuple('Track', d.keys())(*d.values()))

        self.assertEqual('Tema 1', trackResponse.track.trackName)
        self.assertEqual('contenido', trackResponse.track.fileContent)

        putJsonData = {'fileContent': 'nuevo contenido'}
        requests.put('http://localhost:8080/apiv1/tracks/Tema 1', json=putJsonData)
        secondGetAlbumReq = requests.get('http://localhost:8080/apiv1/tracks/Tema 1')
        secondAlbumResponse = json.loads(secondGetAlbumReq.text,
                                         object_hook=lambda d: namedtuple('Track', d.keys())(*d.values()))
        self.assertEqual('Tema 1', secondAlbumResponse.track.trackName)
        self.assertEqual('nuevo contenido', secondAlbumResponse.track.fileContent)

    def tearDown(self):
        requests.delete('http://localhost:8080/apiv1/users/JoseYYY')
        requests.delete('http://localhost:8080/apiv1/tracks/Tema 1')

if __name__ == '__main__':
    unittest.main()