import unittest
import requests

class UserTest(unittest.TestCase):

    def testLoginShouldReturnToken(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "sdAccount@mail.test", "password": "1@drieVierVIJF"})
        self.assertTrue("token" in request.json().keys())

if __name__ == "__main__":
    unittest.main()