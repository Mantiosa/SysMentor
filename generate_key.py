from cryptography.fernet import Fernet

# Encryption key generation
key = Fernet.generate_key()
print("Encryption Key:", key.decode())
