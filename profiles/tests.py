import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

UserProfile = get_user_model()


@pytest.mark.django_db
def test_user_profile_creation():
    """Test creating a UserProfile instance."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123",
        first_name="John",
        last_name="Doe"
    )

    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.is_admin is False
    assert user.date_joined is not None
    assert user.last_login is None
    assert user.avatar is None


@pytest.mark.django_db
def test_user_profile_str():
    """Test the __str__ method of UserProfile."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123"
    )
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_user_profile_get_full_name():
    """Test the get_full_name method of UserProfile."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123",
        first_name="John",
        last_name="Doe"
    )
    assert user.get_full_name() == "John Doe"


@pytest.mark.django_db
def test_user_profile_get_username():
    """Test the get_username method of UserProfile."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123"
    )
    assert user.get_username() == "test@example.com"


@pytest.mark.django_db
def test_user_profile_is_authenticated():
    """Test the is_authenticated method of UserProfile."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123"
    )
    assert user.is_authenticated() is True


@pytest.mark.django_db
def test_user_profile_create_superuser():
    """Test creating a superuser."""
    superuser = UserProfile.objects.create_superuser(
        email="admin@example.com",
        password="admin123"
    )

    assert superuser.email == "admin@example.com"
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.is_admin is True
    assert superuser.is_active is True

@pytest.mark.django_db
def test_user_profile_email_required():
    """Test that email is required for UserProfile."""
    with pytest.raises(ValueError):
        UserProfile.objects.create_user(
            email="",
            password="password123"
        )

@pytest.mark.django_db
def test_user_profile_password_required():
    """Test that password is required for UserProfile."""
    with pytest.raises(ValueError):
        UserProfile.objects.create_user(
            email="test@example.com",
            password=""
        )


@pytest.mark.django_db
def test_user_profile_last_login_updated():
    """Test that last_login is updated on login."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123"
    )
    assert user.last_login is None

    # Simulate a login
    user.last_login = timezone.now()
    user.save()

    assert user.last_login is not None


@pytest.mark.django_db
def test_user_profile_avatar_upload():
    """Test that an avatar can be uploaded for UserProfile."""
    user = UserProfile.objects.create_user(
        email="test@example.com",
        password="password123"
    )
    user.avatar = "avatars/test.jpg"
    user.save()

    assert user.avatar == "avatars/test.jpg"


@pytest.mark.django_db
def test_user_profile_unique_email():
    """Test that email is unique for UserProfile."""
    UserProfile.objects.create_user(
        email="test@example.com",
        password="password123"
    )

    with pytest.raises(ValidationError):
        UserProfile.objects.create_user(
            email="test@example.com",
            password="password123"
        )
