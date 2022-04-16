from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("key_generation.txt", "wb")
file.write(key)
file.close()