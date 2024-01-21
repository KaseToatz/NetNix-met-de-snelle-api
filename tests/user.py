import unittest
import requests
import random

class UserTest(unittest.TestCase):

    def testLoginShouldReturnToken(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "sdAccount@mail.test", "password": "1@drieVierVIJF"})
        self.assertTrue("token" in request.json().keys())

    def testLoginShouldReturn400(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "nonexistinguser", "password": "password"})
        self.assertEqual(request.status_code, 400)

    def testLoginShouldReturn401(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "sdAccount@mail.test", "password": "password"})
        self.assertEqual(request.status_code, 401)

    def testRegisterShouldSucceed(self) -> None:
        request = requests.post("http://localhost/user/register", data={"email": f"newuser{random.randint(0,1000000000)}(@mail.test", "password": "StrongPassword"})
        self.assertEqual(request.status_code, 200)

if __name__ == "__main__":
    unittest.main()