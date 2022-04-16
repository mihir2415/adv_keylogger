from cryptography.fernet import Fernet

key = "Dob7eO5c7tWLRdWQUacP0OZ7jvQngLjE2s1DmovnVGY="

sys = '/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/sys_store_e.txt'
fin = '/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/final_store_e.txt'

encr_files = [sys, fin]
i = 0

for decr in encr_files:
    with open(encr_files[i], 'rb') as f:
        data = f.read()
    
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encr_files[i], 'wb') as f:
        f.write(decrypted)
    i+=1