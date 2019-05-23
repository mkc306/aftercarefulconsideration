from flask import Flask,request,render_template,url_for
import textract
from textblob import TextBlob
import pdb
import os 
from collections import OrderedDict
from operator import itemgetter
from nltk import tokenize
import spacy


#tokenize.sent_tokenize(sentece)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')



def rchop(s, sub):
    return s[:-len(sub)] if s.endswith(sub) else s

	#Load data 
JOB_SPECS = os.listdir("Job_Specs")
with open('skills.txt') as f:
	skills = f.read().split('\n')
	skills = [s.lower() for s in skills]

job_requirements = [textract.process("Job_Specs/" + j).decode('utf8') for j in JOB_SPECS]

resumes = os.listdir('Resumes')

resume_text = [textract.process("Resumes/" + r).decode('utf8').lower() for r in resumes]

nlp = spacy.load('en')

def get_similarity(resume_text,job_nlp):
	#pdb.set_trace()
	cleaned_resume_text =  ' '.join(resume_text)

	doc2 = nlp(cleaned_resume_text)
	return job_nlp.similarity(doc2)



def get_rankings():
	keywords = dict()
	for i in range(len(job_requirements)):
		matches = []
		for word in job_requirements[i].strip().split(" "):
			word = word.lower()
			if word in skills: matches.append(word.lower()) #slow as skills very large 

		#job_name = rchop(JOB_SPECS[i].split("_")[2],".docx") #remove suffix and prefix
		keywords[JOB_SPECS[i]] = set(matches)

	results = dict()

	for job_name,matches in keywords.items():
		scores = []
		score = 0
		job_haha = textract.process("Job_Specs/" + job_name).decode('utf8')
		cleaned_job_text = ' '.join(job_haha.split())
		job_nlp = nlp(cleaned_job_text)
		for i in range(len(resume_text)):
			for keyword in matches:
				if keyword in resume_text[i]:
					score += 1 
			#score = sum([resume_text[i].count(keyword) for keyword in matches ])
			#pdb.set_trace()
			applicant_name = resumes[i].split(".")[0]
			dl_path  ="static/Resumes/" + resumes[i]

			similarity = round(get_similarity(resume_text[i],job_nlp) * 100.0,2)
			#similarity = 0
			scores.append({"name":applicant_name,"score":score,"path":dl_path,"similarity":similarity})
		sorted_scores = sorted(scores,key=lambda i: i["score"],reverse=True)
		sorted_scores = sorted_scores[:10] #only want top 10 scores
		highest_score = sorted_scores[0]["score"]
		for data in sorted_scores:
			data["percentage"] = round((data["score"] / highest_score) * 100.0,2)
			data["combined_score"] = round(((data["percentage"] + similarity) / 2) ,2)
		results[job_name] = sorted_scores
	#pdb.set_trace()
	return results


@app.route('/reports')
def report(results=None):
	results = get_rankings()
	return render_template('report.html',results=results)
    
@app.route('/upload/cv')
def upload_cv():
	return render_template('upload_CV.html')

@app.route('/upload/jd')
def upload_jd():
	return render_template('upload_JD.html')
