from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Profile

# Create your tests here.
class AuthenticationTests(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
    
    def test_register_view(self):
        """
        Test if the register page is accessible and allows
        new user creation.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_validation(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'short',
            'password2': 'short'
        })
        self.assertContains(
            response,
            'Αυτό το συνθηματικό είναι πολύ μικρό. Πρέπει να περιέχει τουλάχιστον 8 χαρακτήρες.'
        )

        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'differentpassword'
        })
        self.assertContains(
            response,
            "Τα δύο πεδία κωδικών δεν ταιριάζουν."
        )

    def test_login_view(self):
        """
        Test if the login page allows user login.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        # Check if user is logged in
        self.assertIn('_auth_user_id', self.client.session)

    def test_failed_login(self):
        """
        Test login with incorrect credentials.
        """
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid username or password.')

    def test_profile_creation(self):
        """
        Check if a Profile Object is created for the user
        """
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_profile_view_access(self):
        # Non-logged-in user should be redirected
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

        #Logged-in user should access the profile page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)