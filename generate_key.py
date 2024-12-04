from cryptography.fernet import Fernet

# Generate an encryption key
key = Fernet.generate_key()
print("Encryption Key:", key.decode())
