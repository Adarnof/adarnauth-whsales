from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, character_id, character_name, email=None, password=None, is_active=True, **extra_fields):
        if email:
            email = self.normalize_email(email)
        user = self.model(character_id=character_id, character_name=character_name, email=email, is_active=is_active, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_user(self, character_id, character_name, email=None, **extra_fields):
        return self._create_user(character_id, character_name, email, **extra_fields)

    def create_superuser(self, character_id, character_name, **extra_fields):
        user = self._create_user(character_id=character_id, character_name=character_name, is_staff=True, is_superuser=True, **extra_fields)
        user.is_active = True
        user.save()
        return user
