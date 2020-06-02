import nltk
from nltk.corpus import stopwords
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def modif(kalimat):
	# nltk.download('punkt')
	pat = ""

	kalimat = kalimat.translate(str.maketrans('','',string.punctuation)).lower() 
	# case folding & menghilangkan tanda baca . ,

	tokens = nltk.tokenize.word_tokenize(kalimat) # tokenization

	fac = StopWordRemoverFactory() #set stopword
	stop = fac.get_stop_words()
	stop.append("kak") #menambahkan "kak" ke dalam kamus stopword

	stop.remove("tidak") #menghapus kata "tidak"
	stop.remove("boleh") #menghapus kata "boleh"
	stop.remove("bisa") #menghapus kata "bisa"
	stop.remove("dimana")
	removed = []
	for t in tokens:
	    if t not in stop:
	        removed.append(t) #stopword removal

	pat = ""

	for w in removed:
	    pat += w+" "


	return(pat)