from flask import Flask,request,render_template,url_for
import textract
from textblob import TextBlob
import pdb
import os 
from collections import OrderedDict
from operator import itemgetter
from nltk import tokenize
import spacy


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



def rchop(s, sub):
    return s[:-len(sub)] if s.endswith(sub) else s

	#Load data 
JOB_SPECS = os.listdir("Job_Specs")
with open('skills.txt') as f:
	skills = f.read().split('\n')
	skills = [s.lower() for s in skills]
job_requirements = [textract.process("Job_Specs/" + j).decode('utf8') for j in JOB_SPECS]

resumes = os.listdir('Resumes')
resumes.remove("Resumes.zip")

resume_text = [textract.process("Resumes/" + r).decode('utf8').lower() for r in resumes]

def get_similarity():
	cleaned_text = [' '.join(r.split()) for r in resume_text]
	#sentences = cleaned_text[0].split('.')
	cleaned_job_text = [' '.join(j.split()) for j in job_requirements]
	nlp = spacy.load('en')
	doc1 = nlp(cleaned_text[1])
	doc2 = nlp(cleaned_job_text[1])
	print(doc1.similarity(doc2))

	#job_spec_sentences = tokenize.sent_tokenize(cleaned_job_text[0])
	#resume_sentences = tokenize.sent_tokenize(cleaned_text[0])



	pdb.set_trace()

def get_rankings():
	keywords = dict()
	for i in range(len(job_requirements)):
		matches = []
		for word in job_requirements[i].strip().split(" "):
			word = word.lower()
			if word in skills: matches.append(word.lower()) #slow as skills very large 
		job_name = rchop(JOB_SPECS[i].split("_")[2],".docx") #remove suffix and prefix
		keywords[job_name] = set(matches)

	results = dict()

	for job_name,matches in keywords.items():
		scores = []
		score = 0
		for i in range(len(resume_text)):
			for keyword in matches:
				if keyword in resume_text[i]:
					score += 1 
			#score = sum([resume_text[i].count(keyword) for keyword in matches ])
			#pdb.set_trace()
			applicant_name = rchop(resumes[i],".docx")
			scores.append({"name":applicant_name,"score":score})
		sorted_scores = sorted(scores,key=lambda i: i["score"],reverse=True)
		sorted_scores = sorted_scores[:10] #only want top 10 scores
		highest_score = sorted_scores[0]["score"]
		for data in sorted_scores:
			data["percentage"] = round((data["score"] / highest_score) * 100.0,2)
		results[job_name] = sorted_scores
	return results


@app.route('/reports')
def report(results=None):
	get_rankings2()
	results = get_rankings()
	return render_template('report.html',results=results)
    
@app.route('/upload/cv')
def upload_cv():
	return render_template('upload_CV.html')

@app.route('/upload/jd')
def upload_jd():
	return render_template('upload_JD.html')
