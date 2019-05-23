from flask import Flask,request,render_template,url_for
import textract
from textblob import TextBlob
import pdb
import os 
from collections import OrderedDict
from operator import itemgetter
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



def rchop(s, sub):
    return s[:-len(sub)] if s.endswith(sub) else s


def get_rankings():
	JOB_SPECS = os.listdir("Job_Specs")
	with open('skills.txt') as f:
		skills = f.read().split('\n')

	skills = [s.lower() for s in skills]

	#results = []
	job_requirements = [textract.process("Job_Specs/" + j).decode('utf8') for j in JOB_SPECS]
	keywords = dict()
	for i in range(len(job_requirements)):
		#match_dict = {JOB_SPECS[i]:matches}
		matches = []
		#pdb.set_trace()
		for word in job_requirements[i].strip().split(" "):
			word = word.lower()
			if word in skills: matches.append(word.lower()) #slow as skills very large 
		job_name = rchop(JOB_SPECS[i].split("_")[2],".docx") #remove suffix and prefix
		keywords[job_name] = matches

	#pdb.set_trace()

	resumes = os.listdir('Resumes')
	resumes.remove("Resumes.zip")
	#resumes.remove("Charles Samuels.doc") 
	print(resumes)	

	resume_text = [textract.process("Resumes/" + r).decode('utf8').lower() for r in resumes]
	results = dict()

	for job_name,matches in keywords.items():
		scores = []
		for i in range(len(resume_text)):
			score = sum([resume_text[i].count(keyword) for keyword in matches ])
			applicant_name = rchop(resumes[i],".docx")
			scores.append({"name":applicant_name,"score":score})
		sorted_scores = sorted(scores,key=lambda i: i["score"],reverse=True)
		sorted_scores = sorted_scores[:10] #only want top 10 scores
		highest_score = sorted_scores[0]["score"]
		for data in sorted_scores:
			data["percentage"] = (data["score"] / highest_score) * 100.0
		pdb.set_trace()
		results[job_name] = sorted_scores
	return results


@app.route('/reports')
def report(results=None):
	results = get_rankings()
	pdb.set_trace()
	return render_template('report.html',results=results)
    
@app.route('/upload/cv')
def upload_cv():
	return render_template('upload_CV.html')

@app.route('/upload/jd')
def upload_jd():
	return render_template('upload_JD.html')
