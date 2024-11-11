def encrypt_text(plaintext, n):
    ans = ""
    # iterate over the given text
    for i in range(len(plaintext)):
        character = plaintext[i]
        
        # check if space is there then simply add space
        if character == " ":
            ans += " "
        elif not character.isalpha():  # Keep non-alphabetical characters unchanged
            ans += character
        # check if a character is uppercase then encrypt it accordingly 
        elif character.isupper():
            ans += chr((ord(character) + n - 65) % 26 + 65)
        # check if a character is lowercase then encrypt it accordingly
        else:
            ans += chr((ord(character) + n - 97) % 26 + 97)
    
    return ans

# Capture user input for plaintext
plaintext = input("Enter a message to be encrypted: ")
n = 15
print("Plain Text is : " + plaintext)
print("Shift pattern is : " + str(n))
print("Cipher Text is : " + encrypt_text(plaintext, n))
