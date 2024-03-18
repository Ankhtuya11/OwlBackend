import bcrypt

# Declaring our password
password = b'GeekPassword'

# Adding the salt to password
salt = bcrypt.gensalt()

# Hashing the password
hashed = bcrypt.hashpw(password, salt)

# printing the salt
print("Salt:")
print(salt)

# printing the hashed password
print("Hashed:")
print(hashed)

# Simulating login, user provides password to be verified
user_provided_password = b'GeekPassword3'

# Checking if the provided password matches the hashed password
if bcrypt.checkpw(user_provided_password, hashed):
    print("Password matched!")
else:
    print("Password does not match!")
