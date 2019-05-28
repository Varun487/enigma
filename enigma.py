import random

class rotor(object):
    ''' Used to define a rotor, the object that has random connections and turns periodically to create encryption'''
    def __init__(self):
        # to create a list of the randomised connections in the rotor
        self.fwd = [i for i in range(1,27)]
        random.shuffle(self.fwd)
        # to generate the other side of connections according to the random connections
        self.rws = [0 for i in range(26)]
        for j in range(26):
            self.rws[self.fwd[j] - 1] = j + 1
        # copy made for decryption so as to maintain the initial random list
        self.fwd_cpy = list(self.fwd)
        self.rws_cpy = list(self.rws)

    def initialise_rotor(self,num,e_d):
        '''Initializes the rotor to the given encryption code'''
        for i in range(1, num):
            if e_d == 'e':
                # rotates the rotor according to the given rotor code (encryption)
                self.fwd.insert(0, self.fwd.pop())
            else:
                # rotates the rotor according to the given rotor code (decryption)
                self.fwd_cpy.insert(0, self.fwd_cpy.pop())

    def rotate(self,e_d):
        '''Manipulates the list to simulate the rotor rotation'''
        if e_d == 'e':
            self.fwd.insert(0, self.fwd.pop())
        else:
            self.fwd_cpy.insert(0, self.fwd_cpy.pop())

    def make_rws(self):
        '''Creates the reverse list according to the forward list.
            Used only in decryption, hence uses only the copy lists.'''
        for j in range(26):
                self.rws_cpy[self.fwd_cpy[j] - 1] = j + 1

# Creating all rotor objects
rotor1 = rotor()
rotor2 = rotor()
rotor3 = rotor()
connection_board = rotor()


def make_switches():
    # creating switch board as a dictionary
    switch_board = {}
    number_of_switches = int(input("Enter the number of switches: "))

    # put the letters to be switched in switch board
    for i in range(number_of_switches):
        char_to_switch = input("Enter the character to be switched: ")
        switched_char = input("Enter the switched character: ")
        switch_board[char_to_switch] = switched_char
        switch_board[switched_char] = char_to_switch
    return switch_board

def change_letter(letter,rotor1,rotor2,rotor3,connection_board):
    '''Traversing through the  rotors and connections board'''
    letter = ord(letter) - 97  # converts letter to corresponding index
    letter = rotor1[letter] - 1  # get index to rotor
    letter = rotor2[letter] - 1
    letter = rotor3[letter] - 1
    letter = connection_board[letter] - 1  # get index, to bonce back to rotor1
    letter = rotor3[letter] - 1
    letter = rotor2[letter] - 1  # get the rotor index of the encrypted letter, outputs the letter
    letter = rotor1[letter] - 1 + 97
    letter = chr(letter)
    return letter


# encrypts the string
def encrypt():

    # Initialises the rotors according to the code entered
    rotor1.initialise_rotor(rotor1_encrypt_code,'e')
    rotor2.initialise_rotor(rotor2_encrypt_code,'e')
    rotor3.initialise_rotor(rotor3_encrypt_code,'e')

    encrypted_string = ''

    for i in range(len(encrypt_message)):
        # letter takes value or the i-1 th letter
        letter = encrypt_message[i]
        # encryption of letter
        encrypted_letter = change_letter(letter,rotor1.fwd,rotor2.fwd,rotor3.fwd,connection_board.fwd)
        # adding encrypted letter to the encrypted string
        encrypted_string += encrypted_letter

        rotor1.rotate('e')  # rotates the rotor1 after each letter
        if (i + 1) % 26 == 0:
            rotor2.rotate('e')  # rotates rotor2 after 1 complete rotation of rotor1
        if (i + 1) % 676 == 0:
            rotor3.rotate('e') # rotates rotor3 after 1 complete rotation of rotor2

    print('original encryption: ',encrypted_string)

    # making a switch board for encryption
    switch_board = make_switches()

    # switching letters in encrypted string according to switchboard
    temp = ''
    for i in encrypted_string:
        if i in switch_board:
            i = switch_board[i]
        temp += i

    encrypted_string = temp

    print("ENCRYPTED STRING IS: ",encrypted_string)


# decrypt
def decrypt():
    # making a switch board for decryption
    switch_board = make_switches()

    # Initiialises the rotors according to decryption code given (should be same as encryption code to get the original string)
    rotor1.initialise_rotor(rotor1_decrypt_code,'d')
    rotor1.make_rws()
    rotor2.initialise_rotor(rotor2_decrypt_code,'d')
    rotor2.make_rws()
    rotor3.initialise_rotor(rotor3_decrypt_code,'d')
    rotor3.make_rws()

    # switching the letters from switch board to get the original encrypted string
    temp = ''
    for letter in decrypt_message:
        if letter in switch_board:
            letter = switch_board[letter]
        temp += letter

    print('temp is : ',temp)

    decrypted_string = ''

    for i in range(len(temp)):
        # letters in temp assigned to varian=ble letter
        letter = temp[i]
        # decrypting the letter to original letter in string
        decrypted_letter = change_letter(letter,rotor1.rws_cpy,rotor2.rws_cpy,rotor3.rws_cpy,connection_board.rws_cpy)
        # adding decrypted letter to decrypted string
        decrypted_string += decrypted_letter

        rotor1.rotate('d') # rotating rotor1 after each letter
        rotor1.make_rws() # creating the appropriate reverse for the rotor

        if (i+1)%26 == 0:
            rotor2.rotate('d') # rotating rotor2 after complete rotation of rotor1
            rotor2.make_rws() # creating the appropriate reverse for the rotor
        if (i+1)%676 == 0:
            rotor3.rotate('d') # rotating rotor3 after complete rotation of rotor2
            rotor3.make_rws() # creating the appropriate reverse for the rotor

    print("DECRYPTED STRING IS: ", decrypted_string)


# input string to encrypt
encrypt_message = input("PLEASE DO NOT ENTER A SPACE OR SPECIAL CHARACTERS\nEnter message to be encrypted: ")

# encryption of each string is unique to code given for each rotor
rotor1_encrypt_code = int(input("Enter the code number for rotor 1 encrypting: "))
rotor2_encrypt_code = int(input("Enter the code number for rotor 2 encrypting: "))
rotor3_encrypt_code = int(input("Enter the code number for rotor 3 encrypting: "))


# calling encrypt function to make encrypted string
encrypt()
print()

# input string to be decrypted
decrypt_message = input("Enter message to be decrypted: ")

# taking the code to decrypt
rotor1_decrypt_code = int(input("Enter the code number for rotor 1 decrypting: "))
rotor2_decrypt_code = int(input("Enter the code number for rotor 2 decrypting: "))
rotor3_decrypt_code = int(input("Enter the code number for rotor 3 decrypting: "))

# calling decrypt function
decrypt()
print()
