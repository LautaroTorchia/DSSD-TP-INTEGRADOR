from .test_setup import TestSetUp

class TestViews(TestSetUp):
    def test_cannot_register_third_party(self):
        """Test cannot register third party without logging in"""
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_view_user_data(self):
        """Test unauthorized user cannot see user data."""      
        response = self.client.post(
            self.user_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_cannot_refresh_token(self):
        """Test unauthorized user cannot refresh token."""      
        response = self.client.post(
            self.token_refresh_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
