# TOKEN GENERATION CODE
#six library for token generation used for password genration
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class TokenGenerator(PasswordResetTokenGenerator):
    # hashing the passwords
    def _make_hash_value(self,user,timestamp):
        return (six.text_type(user.pk)+ six.text_type(timestamp)+six.text_type(user.is_active))
#generating token
generate_token = TokenGenerator()