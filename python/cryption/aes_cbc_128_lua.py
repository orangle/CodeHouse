#coding:utf-8
#orangleliu
#和openresty lua-resty-string 中 aes_cbc_128_iv 方式对应

def AESencrypt(password, plaintext, iv, base64=False):
    import hashlib, os
    from Crypto.Cipher import AES
    KEY_SIZE = 16
    MODE = AES.MODE_CBC

    paddingLength = 16 - (len(plaintext) % 16)
    paddedPlaintext = plaintext+chr(paddingLength)*paddingLength
    cipherSpec = AES.new(password, MODE, iv)
    ciphertext = cipherSpec.encrypt(paddedPlaintext)
    if base64:
        import base64
        return base64.b64encode(ciphertext)
    else:
        return ciphertext.encode("hex")


def AESdecrypt(password, ciphertext, iv, base64=False):
    import hashlib
    from Crypto.Cipher import AES
    BLOCK_SIZE = 16
    KEY_SIZE = 32
    MODE = AES.MODE_CBC

    if base64:
        import base64
        decodedCiphertext = base64.b64decode(ciphertext)
    else:
        decodedCiphertext = ciphertext.decode("hex")

    cipherSpec = AES.new(password, MODE, iv)
    plaintextWithPadding = cipherSpec.decrypt(decodedCiphertext)
    paddingLength = ord(plaintextWithPadding[-1])
    plaintext = plaintextWithPadding[:-paddingLength]
    return plaintext


passwd = "B653E7989522E911"
iv = passwd
content = '''{"origin_sp":"erya","origin_id":"123","origin_ip":"192.168.3.3","timeout":"20151125_072429","vip":"no"}&key=7042b9a6a28fbef8bdb0773a56b3a242'''
res = AESencrypt(passwd, content, iv)
print res
print AESdecrypt(passwd, res, iv)

enstr = '593c8bfe27bc054b114b959c92f40e3617c143642452899436ed9755454219652a6e8ac5d2cc7ffcf2ce700ea02b8dfc'
print AESdecrypt("1234567890123456", enstr, "1234567890123456")

