from pytest import mark
from users.models.user import User


@mark.django_db
class TestUser():

    def test_create_and_get_user(self):
        user = User.objects.create(email='lautaro@hotmail.com', password='somepassword')
        assert user is not None
        getted_user = User.objects.get(id=user.id)
        assert getted_user is not None
        assert user.id == getted_user.id

    def test_set_and_check_password(self):
        user = User()
        PASSWORD = 'This is a super secure password .!'
        user.set_password(PASSWORD)
        assert user.password != PASSWORD
        assert user.check_password('Not the password') is False
        assert user.check_password(PASSWORD) is True

    def test_jwt(self):
        user = User.objects.create(
            name='Testing',
            email='testing@email.com',
            access_level=User.Type.COMMON_USER_TYPE,
            password='SOMESUPERSECUREPASSWORD'
        )
        payload = user.get_payload_from_jwt(user.jwt)
        assert payload['id'] == user.id
        assert payload['name'] == user.name
        assert payload['email'] == user.email
        assert payload['access_level'] == user.access_level
