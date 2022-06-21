import numpy as np, numpy.random
import database as db
import time
import pandas as pd

#Wichtige Variablen deklarieren
timearr = []
timearr2 = []
runs = []
cou = 0
splitlist = [0, 1000, 2000, 3000, 4000, 5000]

#Laufzeitmessungs-Funktion
def measure_time(x):
  global cou
  global timearr
  global timearr2
  
  if x:
    global start
    start = time.perf_counter()
  else:
    
    end = time.perf_counter() - start
    timearr.append(end)
    timearr2.append('Laufzeit {}. Teil: '.format(cou) + str(end))
    cou += 1
    # print(timearr2[cou-1])


#Barcodegenerierungs-Funktion
def barcode_generator(prefix):

  #Wichtige Variablen. Unique Primzahl, Erlaubte Zeichen, Primzahlenauswahl, Random Number Array
  big_prime = 99194853094755497
  map_chars = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X']
  prime_number_sample = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
  
  #Random Number Array zwischen 0 und 31 wird erstellt
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

#Validierungsfunktion für erstellte Barcodes
def barcode_validation():
  
  #Wichtige Variablen: Große Primzahl für Signatur, Erlaubte Zeichen (1-9 & A-X ohne O), Primzahlen, Input-Barcode
  big_prime = 99194853094755497
  char_array = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X']
  prime_number_sample = [7, 11, 0, 13, 17, 19, 23, 29, 31, 37, 41, 43]
  sample_barcode = 'SA2U6TT4UC5I'

  #Prüfsummenvariable
  check_sum = 0



  #Barcode wird gemäß Wertetabelle aufaddiert und mit Primzahlen multipliziert  
  for i in range(len(sample_barcode)):
    if sample_barcode[i] in char_array:
      if i != 2:
        check_sum = check_sum + char_array.index(sample_barcode[i]) * prime_number_sample[i]
    else:
      print('Nicht erlaubtes Zeichen an Stelle {}'.format(i+1))
      return False

  #Wenn Prüfsumme mal Signaturprimzahl modulo 32 die dritte Stelle des Barcodes ergibt, ist Barcode valide, ergo "return True"
  if str(char_array[(check_sum * big_prime) % 32]) == sample_barcode[2]:
    print('Barcode ist valide!')
    return True
  else:
    print('Prüfsumme inkorrekt!')
    return False


#Funktion zur Erstellung und Speicherung in .csv File von n Barcodes (amount = n)
def batch_barcode_gen(batch, amount, splitarray):


    ### TEIL 1 ###
    measure_time(True)
    #Barcode-Set wird erstellt und Barcodes werden reingespeichert
    barcodes = set()
    for i in range(amount):
        barcodes.add(barcode_generator(batch))
    measure_time(False)


    ### TEIL 2 ###
    measure_time(True)

    #Barcode-Set wird in Liste umgewandelt
    barcodes = list(barcodes)

    #Barcode-Liste wird in Pandas-Dataframe konvertiert, gestückelt und anschließend in Excel umgewandelt
    for i in range(len(splitarray)-1):
      if len(barcodes) > splitarray[i]:
        df = pd.DataFrame(barcodes[splitarray[i]:splitarray[i+1]])
        df.to_excel('barcode_batch_' + str(batch) + str(i+1) + '.xlsx', header=False, index=False)

    #Barcode-Liste wird gestückelt und in .CSV-Files umgewandelt
    for i in range(len(splitarray)-1):
      if len(barcodes) > splitarray[i]:
        with open('barcode_batch_' + str(batch) + str(i+1) + '.csv','w') as f:
            np.savetxt(f, barcodes[splitarray[i]:splitarray[i+1]], fmt="%s", delimiter=",")
        f.close()
    measure_time(False)


    ### TEIL 3 ###
    measure_time(True)
    #Barcode-Liste wird für Datenbank in Tupel-Datentyp konvertiert
    barcodes = tuple(barcodes)
    data = [x for x in zip(*[iter(barcodes)])]
    data = (', '.join('("{}")'.format(t[0]) for t in data))[1:-1]
    measure_time(False)


    ### TEIL 4 ###
    measure_time(True)
    #Barcode-Tupel wird in Datenbank gespeichert
    c_conn, c_curs = db.connect_db()
    c_curs.execute("INSERT INTO barcode_recs(barcode) VALUES({});".format(data))
    c_conn.commit()
    measure_time(False)

    #Laufzeitkontrolle
    print('Gesamtlaufzeit:   ' + str(sum(timearr)))
    for i in range(len(timearr)):
      print(str(i+1) + '. Teil, Laufzeitanteil: ' + str(round(timearr[i]/sum(timearr)*100)) + ' %')
    timearr.clear()
    timearr2.clear()
    


#Ausgelegt für Batches à 3 Mio. Barcodes.
def generate_multiple_batches(codes_per_batch, splitarray, batches):

  #Variablen für Batcherstellung. Wichtig: 'batches'-items MÜSSEN 2 Zeichen lang sein! z.b. ("SA", "AB", "XY")
  #Anzahl der Items in 'batches' definiert Anzahl der zu generierenden Batches
  filenameArray = []
  string = "barcode_batch_"
  numarr = list(range(1,(len(splitarray))))

  #Erstellt Dateinamen
  for x in batches:
      for y in numarr:
          filenameArray.append(string + x + str(y))
  
  #Barcodegenerator rennt für festgelegte Zahl an Barcodes pro festgelegter Zahl an Batches (hier: 6 Batches à 3 Mio. Barcodes)
  for i in filenameArray:
    batch_barcode_gen(batches[filenameArray.index(i) % len(batches)], codes_per_batch, splitarray)

# generate_multiple_batches()
# barcode_validation()


if __name__ == "__main__":

  #codes_per_batch = Barcodes pro Batch
  #splitarray = Stückelungsarray für CSV/PDF: bspw. [0, 1000, 2000] hat 2 Files, Barcodes von 0 bis 1000 und von 1000 bis 2000
  #batches = Hier können Namen und Anzahl der Batches festgelegt werden.

  generate_multiple_batches(codes_per_batch = 5000, splitarray = [0, 1000, 2000, 3000, 4000, 5000], batches = ["SA","SB","SC","SD","SE","SF"])
  