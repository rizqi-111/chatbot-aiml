import sys
import aiml
from mysql.connector import MySQLConnection
import datetime
import mgr_6_11_19 as mgr
import tes_nltk as tnltk

kernel2 = aiml.Kernel()
kernel2.learn("ask.aiml")

a = str(sys.argv[1]) #id_pertanyaan 
b = str(sys.argv[2]) #jawaban
    
now = datetime.datetime.now()
n = str(now)
mydb = MySQLConnection(
	host = "localhost",
	user = "root",
	passwd = "",
	database = "chat"
	)

myc = mydb.cursor()

myc.execute("SELECT teks FROM chat WHERE id_chat = "+a)
result_set = myc.fetchall()
for row in result_set:
    pertanyaan = row[0]

mgr.append_pattern('ask.aiml',tnltk.modif(pertanyaan),str(b))