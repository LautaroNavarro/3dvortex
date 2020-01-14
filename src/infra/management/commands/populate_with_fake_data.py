from django.conf import settings
from django.core.management.base import BaseCommand
from users.models.user import User
from models.models.category import Category
from image_medias.models.image_media import ImageMedia
from model_medias.models.model_media import ModelMedia
from models.models.model import Model
import random


PATH_TO_FILE = '~/personal/3dvortex/src/infra/management/commands/populate_with_fake_data.py'

users_dict = [
    {
        'email': 'facundo@hotmail.com',
        'password': 'facuTobares123!',
        'name': 'Facundo',
        'lastname': 'Tobares',
    },
    {
        'email': 'florencia@hotmail.com',
        'password': 'florTobares123!',
        'name': 'Florencia',
        'lastname': 'Tobares',
    },
    {
        'email': 'cristian@hotmail.com',
        'password': 'cristanMoyano123!',
        'name': 'Cristan',
        'lastname': 'Moyano',
    },
    {
        'email': 'octavio@hotmail.com',
        'password': 'octavioCoria123!',
        'name': 'Octavio',
        'lastname': 'Coria',
    }
]

categories_list = [
    'Exterior',
    'Interior',
    'Animales',
    'Arquitectura',
    'Autos',
    'Comida',
    'Electronica',
    'Muebles',
    'Ciencia',
    'Spacio',
    'Vehiculos',
    'Varios',
    'Deportes',
]


class Command(BaseCommand):
    help = 'Populate the db with fake data'

    @staticmethod
    def create_user(email, name, lastname, password):
        user = User(
            email=email,
            name=name,
            lastname=lastname,
            status=User.Status.CONFIRMED_STATUS.value,
            access_level=User.Type.COMMON_USER_TYPE.value,
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def create_image_media(user, data):
        image_media = ImageMedia.objects.create(user=user)
        return image_media.upload_image(data)

    @staticmethod
    def create_model_media(user):
        # TODO: Implement
        return ModelMedia.objects.create(
            user=user,
            url='https://fake.url.com'
        )

    @classmethod
    def create_models_for_user(cls, user, categories):
        image_names = [
            'arquera.png',
            'caballero.jpeg',
            'enano.png',
            'gohan.jpg',
            'hulk.jpg',
            'humano.png',
            'mask.jpg',
            'star-wars.png',
        ]
        models = []
        for image_name in image_names:
            data = open('infra/management/commands/statics/{}'.format(image_name), 'rb')
            image_media = cls.create_image_media(user, data)
            model_media = cls.create_model_media(user)
            models.append(Model.objects.create(
                user=user,
                name=image_name,
                description='',
                model_media=model_media,
                image_media=image_media,
                privacy=Model.Privacy.PUBLIC.value,
                category=random.choice(categories),
            ))
        return models

    @staticmethod
    def create_categories():
        categories = []
        for category_string in categories_list:
            categories.append(Category.objects.create(name=category_string))
        return categories

    def create_printers():
        pass

    def handle(self, **kwargs):
        categories = self.create_categories()
        users = []

        for user_dict in users_dict:
            user = self.create_user(**user_dict)
            users.append(user)
            self.create_models_for_user(user, categories)
