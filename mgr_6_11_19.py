import re
import aiml
import csv

cl = "</aiml>"
term = "<pattern>"
end = "</pattern>"
cat = "<category>\n"
cat2 = "</category>\n\n" + cl
temp = "\n<template>"
temp2 = "</template>\n"

def get_index(filename,sentences): #parameter berupa kata yg ingin dicari list dan nama file aiml
    file = open(filename) #open file untuk membaca
    
    con = file.readlines() #menyimpan file ke dalam list
    idx = con.index(sentences) #mendapatkan index template yg diinginkan
    return  idx

def print_pattern(filename): #parameter berupa filename
    term = "<pattern>" #inisialisasi variabel dengan string tag pattern
    end = "</pattern>" #inisialisasi variabel dengan string tag tutup pattern
    pattern = [] #inisialisasi variabel list 
    file = open(filename) #open file untuk membaca
    for line in file: #mengisi variabel line dengan isi file
        if term in line: #jika ditemukan term pada line saat ini
            a = line[:line.find(end)] #memotong </pattern>
            b = re.split(term,a) #memotong <pattern>
            pattern.append(b[1]) #menambahkan b[1] ke dalam list pattern
    file.close() #menutup file
    return pattern

def append_pattern(filename,pattern,template): #parameter berupa filename,pattern,template
    cat = "<category>\n" #inisialisasi variabel dengan string tag category
    term = "<pattern>" #inisialisasi variabel dengan string tag pattern
    end = "</pattern>" #inisialisasi variabel dengan string tag tutup pattern
    temp = "\n<template>" #inisialisasi variabel dengan string tag template
    temp2 = "</template>\n" #inisialisasi variabel dengan string tag tutup template
    cat2 = "</category>\n\n</aiml>" 
    #inisialisasi variabel dengan string tag tutup category dan tag tutup aiml

    file = open(filename) #open file untuk membaca
    
    con = file.readlines() #menyimpan file ke dalam con (list)
    idx_end = get_index(filename,cl) #mendapatkan index cl (</aiml>)

    f = open(filename,"w") #open file untuk append (menambahkan teks)

    con[idx_end] = cat+term+pattern+end+temp+template+temp2+cat2 
    #variabel con menyimpan string pattern dan template baru
    f.writelines(con) #menuliskan con ke dalam file aiml
    file.close() #menutup file
    f.close() #menutup file

def replace_template(filename): #parameter berupa pattern atau tempalte yg diubah
    file = open(filename) #open file untuk membaca
    
    con = file.readlines() #menyimpan file ke dalam list
    idx_temp = get_index(filename,"<template>no answer</template>"+"\n") #mendapatkan index template yg diinginkan

    f = open(filename,"w") #open file untuk menulis teks

    con[idx_temp] = "<template>"+"blalalalacccc"+temp2
    f.writelines(con)
    file.closef
    f.close

def clear_aiml(filename):
    file = open(filename,"r+") #open file untuk membaca
    file.truncate(0)
    header = '<aiml version="1.0.1" encoding="UTF-8">\n\n</aiml>'
    file.writelines(header)
    file.close()

def make_regex(pattern): #parameter berupa pattern aiml (string)
    list = re.split("\s",pattern) #memotong \s (spasi) pada kalimat pattern
    s = "" #inisialisasi variabel s (string)
    
    for x in list: #mengisi variabel x dengan list
        if (x != "*"): #jika ditemukan "*" maka tidak dimasukkan dalam s
            if (len(s) != 0): 
                s += "|" # "|" ditambahkan jika s tidak kosong
            s += x #menambahkan x ke dalam s

    if not s: #jika s kosong
        reg = ""
    else:
        reg = re.compile(s,re.VERBOSE)
    return (reg)

def leng_str(stri):
    a = re.split("\s",stri)
    return (len(a))

def get_percent(pattern,question): #parameter berupa pattern (string) dan pertanyaan
    x = 0 #inisialisasi variabel persentase similaritas
    reg = make_regex(pattern)  #mengubah pattern (string) ke dalam format regex
    if reg: #jika reg tidak kosong
        m = re.findall(reg,question) #mencari kata dalam reg pada question
        y = set(m) #menghapus duplicate tuples from list
        # print("m = ",m)
        if '' in y:
            y.remove('')
        if not y: #jika y kosong
            x = 0 
            return x
        
        n = len(y) #menghitung jumlah / banyak kata(pattern) yg ditemukan pada question
        p = leng_str(pattern) #menghitung jumlah / banyak kata dalam pattern
        # print("y = ",y)
        # print("n = ",n," p = ",p)
        x = round(((n / p)*100),2)
        # print("regex = ",reg)
    return x

def get_respon(filename, question): #parameter berupa filename (string) dan question (string)
    kernel = aiml.Kernel() #memanggil kelas kernel pada library aiml
    kernel.learn(filename) #mengisi dan mempelajari isi file aiml kepada kernel
    threshold = 55.00 #inisialisasi variabel nilai ambang batas similaritas
    max1 = 0.00 #inisialisasi variabel nilai similaritas tertinggi
    v1 = "" #inisialiasi variabel string pattern dengan nilai similaritas tertinggi
    b = print_pattern(filename) #menyimpan seluruh pattern pada file aiml ke dalam b
    for v in b: #mengisi variabel b ke dalam v
        value = get_percent(v,question) #menyimpan nilai similaritas ke dalam value
        # print("Pattern = ",v,"\nNilai = ",value,"\n") 
        if(max1 <= value): #jika value lebih besar dari nilai tertinggi saat ini
            #print("v = ",v,"value = ",value) 
            max1 = value #nilai tertinggi saat ini berubah
            v1 = v #variabel string pattern berubah
    if(max1 >= threshold): #jika nilai similaritas lebih dari threshold
        result = (kernel.respond(v1),v1,max1) #mengabil respon/template dengan pattern v1 dalam kernel 
    else: #jika tidak ditemukan kemiripan atau nilai similaritas kurang dari threshold
        result = (1)
        #pertanyaan disimpan di database untuk dikirimkan ke pakar
    return result

# with open('hasil_ask.csv','w') as f: #untuk menulis hasil test ke csv
#     writer = csv.writer(f)
#     result_test = print_pattern("ask.aiml")
    
#     writer.writerow(result_test)

def retrieve2(question):
    max1 = max2 = max3 = 0.00
    v1 = v2 = v3 = ""
    b = print_pattern("ask.aiml")
    for v in b:
        value = get_percent(v,question)
        if(max1==0.00 and max2==0.00 and max3==0.00):
            max1 = value
        elif(max1 < value):
            max2 = max1
            max1 = value
            v2 = v1
            v1 = v
        elif(max2 < value):
            max3 = max2
            max2 = value
            v3 = v2
            v2 = v
        elif(max3 < value):
            max3 = value
            v3 = v
    #     print (v , " : ",value)
    # print(max1,max2,max3)
    # print("V1 = ",v1,"V2 = ",v2,"V3 = ",v3)
    result = (v1,max1,v2,max2,v3,max3)
    return result