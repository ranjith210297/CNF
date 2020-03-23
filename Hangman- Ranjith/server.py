import socket
import random

'''
This method will display us the remianing available letters from the alphabets that rae not guessed.
'''
def getAvailableletter(guessed_letters,no_of_guesses):
 

  global alphabets
  global incorrect
  for i in guessed_letters:
    if i in secret_word:
      conn.sendall("good guess.\n".encode())
      alphabets.remove(i)
    else:
      no_of_guesses=no_of_guesses-1
      incorrect=incorrect+1
      alphabets.remove(i)
      conn.sendall("incorrect guess.\n".encode())
  return "".join(alphabets),no_of_guesses


def getguessword(secret_word,lettersGuessed):
    '''
    Method to display the guessed word from the user thats been choosed randomly by server only the matched 
    letters are displayed otherwise "_" is printed in that letters place..
    '''

    a=secret_word

    for d in secret_word:
      if d not in lettersGuessed :
         a=a.replace(d," _")
    if a==secret_word:
      conn.sendall("\nyou won! ".encode())
      return
    else:
      return(a)

'''
Method to check whther the word is correct or not.
@param secret_word,guessed_letters,l
'''
def isWordguessed(secret_word,guessed_letters,l):
  
  no_of_guesses = 8
  length = l
  #conn.sendall(secret_word)
  lettersGuessed = []
  nums = '123456789!@#$%^&*()? /'
  num_special_chars = list(nums)
  conn.sendall(f'\nI am thinking of a word contains letters is {l}\n'.encode())
  while no_of_guesses != 0:
    global alpha
    conn.sendall(f'\nYou have {str(no_of_guesses)} guesses left\n'.encode())
    G = conn.sendall('\nplease guess a letter:1'.encode())
    G = conn.recv(1024).decode()
    G= G.lower()
    if (G in  alphabets) and len(G)==1 :
      guessed_letters=[G]
      lettersGuessed = lettersGuessed+[G]
      let,no_of_guesses = getAvailableletter(guessed_letters,no_of_guesses)
      conn.sendall(f'{let}\n'.encode())
      if getguessword(secret_word,lettersGuessed):
        conn.sendall(f'{getguessword(secret_word,lettersGuessed)}\n'.encode())
      else:
        break
    else:
      if len(G)>1:
        conn.sendall('only one letter\n'.encode())

      elif(G  in num_special_chars):
        conn.sendall("Invalid input\n".encode())
      else:
        conn.sendall("Oops! letter already guessed\n".encode())


  else:
    conn.sendall("game over-You lost\n".encode())
    conn.sendall(f"secretWord is {secret_word}".encode())

def hangman(secret_word,guessed_letters,l):
  isWordguessed(secret_word,guessed_letters,l)


players = {'Ranjith' : 5,'Kumar' : 12}
score = 0
incorrect = 0
lea_board = ""
guessed_letters=[]
lettersGuessed=[]

# for reading the file and choosing a random word from the list of words from the file.
text_file = open("words.txt", "r")
lines = text_file.readlines()
for i in lines:
    wordlist = i.split()

secret_word = random.choice(wordlist)




l=len(secret_word)

letters = 'abcdefghijklmnopqrstuvwxyz'
alphabets= list(letters)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    soc.bind(('192.168.0.105',8080))
    soc.listen(5)
    while True:
        conn,addr = soc.accept()
        option = conn.recv(1024).decode() 
        if option == '1':  
            newUser = conn.recv(1024).decode()
            players[newUser] = 0
            conn.sendall("start".encode())
            hangman(secret_word,guessed_letters,l)
            score = ((10*len(secret_word)) - (incorrect*len(secret_word)))
            players[newUser] = score
        else: 
            userName = conn.recv(1024).decode()
            if userName in players :
                conn.sendall("start".encode())
                hangman(secret_word,guessed_letters,l)
                score = ((10*len(secret_word)) - (incorrect*len(secret_word)))
                players[userName] = score
                conn.sendall("start".encode())

            else:
                players[userName] = 0
                conn.sendall("start".encode())
                hangman(secret_word,guessed_letters,l)
                score = ((10*len(secret_word)) - (incorrect*len(secret_word)))
                players[userName] = score
                conn.sendall("start".encode())
        sorted(players.values())
        for key,value in players.items():
            lea_board = lea_board + key +" "+str(value)+"\n"
        conn.sendall(("\n****Leader Board****\n"+lea_board).encode())

