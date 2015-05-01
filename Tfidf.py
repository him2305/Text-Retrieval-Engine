import nltk, zipfile, re, math, time
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords # Import the stop word list
from nltk.stem.snowball import SnowballStemmer # stemmer 
from nltk.stem import  WordNetLemmatizer

#Calculating the TF-IDF of documents
def stem_lemmatize(word):
	stemmer = SnowballStemmer("english")
	word = stemmer.stem(word)
	return word
def word_list(words):
	lst = []
	letters_only = re.sub("[^a-zA-Z]", " ", words) 
	words = letters_only.lower().split()                             
	stops = set(stopwords.words("english"))                  
	meaningful_words = [w for w in words if not w in stops]
	
	for words in meaningful_words:
		words =  stem_lemmatize (words)
		lst.append(words)
	return lst
	
def review_to_words( dict,raw_review,fName, wordList ):
	lst = []
	uLst = []
	lst = word_list(raw_review.decode())
	#uLst = set(lst)
	uLst = lst
	fName2 = fName.split('/')
	fName2 = fName2[2];
	dict[fName2] = [];
	#dict[fName2].append(uLst)
	uniqueList = set(uLst)
	docDict = {}
	for eachWord in uniqueList:
		 wordCount = uLst.count(eachWord)
		 docDict [eachWord] = 1 + math.log(wordCount , 2)
		 wordList.append(eachWord)
	dict[fName2]= docDict
	
unqiuelist = []
print ('start' , time.strftime("%H:%M:%S"))
documentDictionary = {}
wordList = []
with zipfile.ZipFile('proj1data2.zip', 'r') as zfile:
    for name in zfile.namelist():
  			if name.find("blogs/B") >=0:
  				f = zfile.open(name).read()
  				clean_review = review_to_words(documentDictionary, f , name , wordList)
  				print(name)
print ('READ ALL THE DOCUMENTS', time.strftime("%H:%M:%S"))
bagOfWords = set(wordList)
documentCount = len(documentDictionary)
documentKeys = documentDictionary.keys()
dictIDF = {}
for word in bagOfWords:
	wordCount = 0
	for dKeys in documentKeys:
		if word in documentDictionary[dKeys]:
			wordCount+=1
	dictIDF[word] = math.log(documentCount/ (1+wordCount) , 10)
tfidf={}
for word in bagOfWords:
	wordCount = 0
	docDict = {}
	for dKeys in documentKeys:
		if word in documentDictionary[dKeys]:
			docDict[dKeys] = dictIDF[word] * documentDictionary[dKeys][word]
			
	tfidf[word] = docDict

print ('TFIDF COMPLETED ', time.strftime("%H:%M:%S"))

#Calculating TF-IDF of Query

queryResultDict = {}
queryDICT = { 
				'851':'March of the Penguins' , '852':'larry summers' , '853':'state of the union' , 
				'854': 'Ann Coulter', '855' :'abramoff bush' , '856':'macbook pro','857' : 'jon stewart',
				'858':'super bowl ads','859':'letting india into the club?','860':'arrested development',
				'861':'mardi gras','862':'blackberry','863':'netflix','864':'colbert report',
				'865':'basque', '866':'Whole Foods', '867': 'cheney hunting', '868':'joint strike fighter',
				'869':'muhammad cartoon','870':'barry bonds','871':'cindy sheehan','872':'brokeback mountain',
				'873':'bruce bartlett','874':'coretta scott king', '875':'american idol', '876':'life on mars',
				'877':'sonic food industry', '878':'jihad', '879':'hybrid car','880':'natalie portman',
				'881':'Fox News Report', '882':'seahawks', '883':'heineken','884':'Qualcomm','885': 'shimano', '886':'west wing',
				'887':'World Trade Organization', '888': 'audi', '889':'scientology','890':'olympics' , '891':'intel','892':'Jim Moran',
				'893':'zyrtec', '894':'board chess', '895':'Oprah', '896':'global warming' , '897': 'ariel sharon','898':'Business Intelligence Resources',
				'899': 'cholesterol', '900':'mcdonalds'
			}
			



for qr in queryDICT:
	print ('QUERY Processing : ', time.strftime("%H:%M:%S"))
	print (queryDICT[qr])
	queryResultDict[qr] = []
	query = queryDICT[qr]
	lst = word_list(query)
	count = 0
	docDict = {}
	for synset in wn.synsets(query):
 		for lemma in synset.hypernyms():
 			unqiuelist = lemma.name()
			
	uniqueList = set(lst)
	for eachWord in uniqueList:
		 wordCount = lst.count(eachWord)
		 docDict [eachWord] = wordCount

	sim={}
	tempList={}
	dict={}
	sum = 0
	for partialQuery in docDict:
		if partialQuery in tfidf:
			tempList=tfidf[partialQuery].keys()		
			for key in tempList:
				if key not in dict:
					dict[key] = []
				dict[key].append(tfidf[partialQuery][key] * docDict[partialQuery])
	resultDict = {}
	sum = 0
	sum1 = 0
	for doc,values in dict.items():
		for value in values:
			sum += value
		wordsFreq = documentDictionary[doc]
		for wordTF in wordsFreq:
			sum1 += wordsFreq[wordTF] * wordsFreq[wordTF]
		divide = math.sqrt(sum1)
		sim = sum / divide
		angle = math.acos(sim)
		if angle not in resultDict:
			resultDict[angle] = []
		resultDict[angle].append(doc)
	ang = list(resultDict.keys())
	ang.sort()
	for docret in ang:
		queryResultDict[qr].append(resultDict[docret])

print(queryResultDict)
	
#query Extension

