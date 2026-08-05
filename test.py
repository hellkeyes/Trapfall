import string
import secrets

characters = string.ascii_uppercase + string.digits
x = 'TRAP' + '-' +  "".join(secrets.choice(characters) for _ in range(4))

print(x)