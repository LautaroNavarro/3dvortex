from django.test import TestCase
from users.models.user import User


class TestUser(TestCase):

    def test_create_and_get_user(self):
        user = User.objects.create(email='lautaro@hotmail.com', password='somepassword')
        self.assertIsNotNone(user)
        getted_user = User.objects.get(id=user.id)
        self.assertIsNotNone(getted_user)
        self.assertEqual(user.id, getted_user.id)

    def test_set_and_check_password(self):
        user = User()
        PASSWORD = 'This is a super secure password .!'
        user.set_password(PASSWORD)
        self.assertNotEqual(user.password, PASSWORD)
        self.assertFalse(user.check_password('Not the password'))
        self.assertTrue(user.check_password(PASSWORD))
