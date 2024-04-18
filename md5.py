import hashlib

dpassw = 'd9b1d7db4cd6e70935368a1efb10e377'


passw = '123'
asd = hashlib.md5(hashlib.md5(passw.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
print(asd,dpassw)