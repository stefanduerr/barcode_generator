import pandas as pd
import pdfkit
from requests import head
from barcode_gen import measure_time
import multiprocessing
from barcode_gen import splitlist

#SEHR SPEZIFISCH; MUSS JE NACH DATEINAMEN ANGEPASST WERDEN!
#Deklarierung wichtiger Variablen
#CSV-DATEINAMEN MÜSSEN STRINGS IN "fileNameArray" ENTSPRECHEN!

filenameArray = []                            # Gesamtes Namenarray (hier: ["barcode_batch_SA1", "barcode_batch_SA2", "barcode_batch_SA3", ...])
string = "barcode_batch_"                     # 1. Teil des Namens
filename = ["SA","SB","SC","SD","SE","SF"]    # 2. Teil des Namens: Batch-Endung
numarr = list(range(1,(len(splitlist))))      # 3. Teil des Namens: Stückelung in n Codes / Batch (siehe Variable "splitlist")

#Befüllung des Namenarrays
for x in filename:
    for y in numarr:
        filenameArray.append(string + x + str(y))

#CSV Files in PDF Files umwandeln (Parameter x = Namenarray)
def csv_to_pdf(x):
    measure_time(True)
    csv = x + '.csv'
    html_file = csv[:-3]+'html'

    df = pd.read_csv(csv, sep=',', header=None)
    df.index += 1
    
    df.to_html(html_file, header=False)
    measure_time(False)
    print('html conversion of ' + x + ' complete')    

    measure_time(True)
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdfkit.from_url(x + ".html", x + "_pdf.pdf", configuration=config)
    measure_time(False)
    print('pdf conversion of ' + x + ' complete')  


if __name__ == "__main__":

    #Hier Prozessorkerne festlegen
    cores = 8

    #Für bessere Performance wurde hier Multicore-Processing eingebaut.
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(cores)
    pool.map(csv_to_pdf, filenameArray)
