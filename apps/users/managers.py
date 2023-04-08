from django.contrib.auth.models import (
    BaseUserManager
)


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password,
                    first_name,
                    last_name,
                    phone_number=None,
                    **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email or not username:
            raise ValueError('Users must have an email and username ')

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email,
        username and password.
        """
        user = self.create_user(
            password=password,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_sponsor = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
