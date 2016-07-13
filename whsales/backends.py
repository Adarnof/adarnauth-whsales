from whsales.models import User

class TokenAuthenticationBackend(object):
    def authenticate(self, token=None):
        if not token:
            return None
        try:
            return User.objects.get(character_id=token.character_id)
        except User.DoesNotExist:
            user = User.objects.create_user(character_id=token.character_id, character_name=token.character_name)
            return user
        except:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
