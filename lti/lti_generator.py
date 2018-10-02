import os
print('key')
print(os.urandom(16).hex())
print()
print('secret')
print(os.urandom(32).hex())
