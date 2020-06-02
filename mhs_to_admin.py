import sys
import aiml
from mysql.connector import MySQLConnection
import datetime
import mgr_6_11_19 as mgr

kernel2 = aiml.Kernel()
kernel2.learn("ask.aiml")

a = str(sys.argv[1])
b = str(sys.argv[2])

x = mgr.get_respon("ask.aiml",a)

if x != 1:
	ans = "BOT : "+x[0]
else :
    ans = "BOT : Mohon tunggu sebentar, Tim PMB akan menjawab Pertanyaan Anda"
    
print("x = ",a)

now = datetime.datetime.now()
n = str(now)
mydb = MySQLConnection(
	host = "localhost",
	user = "root",
	passwd = "",
	database = "chat"
	)

myc = mydb.cursor()

myc.execute("SELECT * FROM chat WHERE pengirim = '"+str(b)+"' ORDER BY waktu DESC LIMIT 1")
result_set = myc.fetchall()
for row in result_set:
    idchat = row[0]

sql = "INSERT INTO chat (id_reply,pengirim,penerima,waktu,teks,statuss) VALUES ("+str(idchat)+",'admin','"+str(b)+"','"+n+"',' "+str(ans)+"',1)"
myc.execute(sql)

mydb.commit()