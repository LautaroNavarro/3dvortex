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
