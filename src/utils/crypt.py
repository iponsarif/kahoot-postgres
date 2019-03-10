# encrypt pake caesar chiper
shift = 2
alphanumeric = 'abcdefghijklmnopqrstuvwxyz0123456789'
listAlphanumeric = list(alphanumeric)

def encrypt(password):
    listPassword = list(password)    
    
    for i in range(len(listPassword)):
        charPosition = listAlphanumeric.index(listPassword[i])
        newPosition = (charPosition + shift) % len(listAlphanumeric)
        listPassword[i] = listAlphanumeric[newPosition]
    
    encryptedPassword = ''.join(listPassword)    
    return encryptedPassword

# decrypt pake caesar chiper
def decrypt(password):
    listPassword = list(password)
    
    for i in range(len(listPassword)):
        charPosition = listAlphanumeric.index(listPassword[i])
        newPosition = (charPosition - shift) % len(listAlphanumeric)
        listPassword[i] = listAlphanumeric[newPosition]
    
    decryptedPassword = ''.join(listPassword)    
    return decryptedPassword