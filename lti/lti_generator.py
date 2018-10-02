import os

# Generates a new key and secret couple for the lti Oauth communication te key
# and secrect are generated according to the guidelines given in
# https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/

print('LTI_KEY:')
print(os.urandom(16).hex())
print()
print('LTI_SECRET:')
print(os.urandom(32).hex())
