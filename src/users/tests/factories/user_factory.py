import factory
from users.models.user import User
from users.helpers.date_helpers import get_current_utc_datetime


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    name = factory.Sequence(lambda n: 'name_{}'.format(n))
    lastname = factory.Sequence(lambda n: 'lastname_{}'.format(n))
    email = factory.LazyAttribute(lambda o: '{}s@3dvortex.org'.format(o.name))
    password = factory.Sequence(lambda n: 'pass_{}'.format(n))
    status = User.Status.CONFIRMED_STATUS.value
    access_level = User.Type.COMMON_USER_TYPE.value
    mercado_pago_id = factory.Sequence(lambda n: 'id_{}'.format(n))
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        kwargs['password'] = User.hash_password(kwargs['password'])
        return kwargs
