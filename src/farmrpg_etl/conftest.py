import pytest


@pytest.fixture(scope="session")
def django_db_modify_db_settings(django_db_modify_db_settings):
    from django.conf import settings

    del settings.DATABASES["game_prod"]
    del settings.DATABASES["game_alpha"]
