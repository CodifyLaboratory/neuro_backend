from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_active, is_simple_user, is_professor, is_staff, is_superuser,
                     **extra_fields):
        if email:
            email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            email=email,
            is_simple_user=is_simple_user,
            is_active=is_active,
            is_superuser=is_superuser,
            is_professor=is_professor,
            date_joined=now,
            is_staff=is_staff,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, False, False, False, **extra_fields)

    def create_admin(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, False, True, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, True, False, False, True, True, **extra_fields)
        user.save(using=self._db)
        return user


