from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        return (six.text_type(email) + six.text_type(timestamp)) 

account_activation_token = AccountActivationTokenGenerator()

