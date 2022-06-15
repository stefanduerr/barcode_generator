import numpy as np, numpy.random

def barcode_generator(prefix):

  #Wichtige Variablen. Unique Primzahl, Erlaubte Zeichen, Primzahlenauswahl, Random Number Array
  big_prime = 99194853094755497
  map_chars = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X']
  prime_number_sample = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
  arrc = np.random.randint(32, size=9)

  #Prefixarray wird erstellt und Präfix auf Werte umgemappt
  prefix_arr = np.array([])
  for i in range(len(prefix)):
    if prefix[i] in map_chars:
      prefix_arr = np.insert(prefix_arr, i, map_chars.index(prefix[i]))
    else:
      print('Invalid Batch')
      return False
  
  #Präfixarray wird mit Random Number Array vereinigt
  arrc = np.insert(arrc, 0, prefix_arr)
  #Arraykombination wird mit Primzahlenauswahl multipliziert
  cs_arr = np.multiply(arrc, prime_number_sample)

  #Checksummenwert wird erstellt und umgemappt
  chksm = (sum(cs_arr) * big_prime) % 32
  chksm = map_chars[chksm]
  
  #Gesamtes Array mit Präfix, Checksumme und Barcode wird in String umgewandelt
  string = ''
  for i in range(len(arrc)):
    if i == 2:
      string = string + chksm
      string = string + map_chars[int(arrc[i])]
    else:
      string = string + map_chars[int(arrc[i])]

  #Barcodestring wird zurückgegeben
  return string

def barcode_validation():
  
  #Wichtige Variablen: Erlaubte Zeichen (1-9 & A-X ohne O), Primzahlen, Testbarcode
  big_prime = 99194853094755497
  char_array = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X']
  prime_number_sample = [7, 11, 0, 13, 17, 19, 23, 29, 31, 37, 41, 43]
  sample_barcode = barcode_generator('SA')

  #Prüfsummenvariable
  check_sum = 0

  #Barcode wird gemäß Wertetabelle aufaddiert und mit Primzahlen multipliziert  
  for i in range(len(sample_barcode)):
    if sample_barcode[i] in char_array:
      if i != 2:
        check_sum = check_sum + char_array.index(sample_barcode[i]) * prime_number_sample[i]

  print(char_array[(check_sum * big_prime) % 32])
  print(sample_barcode[2])
  #Hex-Umwandlung und Prüfung
  if str(char_array[(check_sum * big_prime) % 32]) == sample_barcode[2]:
    return True
  else:
    return False

print(barcode_validation())

#Funktion zur Erstellung und Speicherung in .csv File von n Barcodes (amount = n)
def batch_barcode_gen(amount):

    #Barcode-Set wird erstellt und Barcodes werden reingespeichert
    barcodes = set()
    for i in range(amount):
        barcodes.add(barcode_generator('SA'))

    #Barcode-Set wird in .csv File umgewandelt      
    with open('barcodes.csv','w') as f:
        np.savetxt(f, list(barcodes), fmt="%s", delimiter=",")
    f.close()

batch_barcode_gen(1000)