import textract
from textblob import TextBlob
import pdb
import os 
from collections import OrderedDict
from operator import itemgetter

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
	job_name = JOB_SPECS[i].split("_")
	
	keywords[JOB_SPECS[i]] = matches
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
		scores.append({"name":resumes[i],"score":score})
	sorted_scores = sorted(scores,key=lambda i: i["score"],reverse=True)
	results[job_name] = sorted_scores
#print results in descending order 

#sorted_results = sorted(,key = itemgetter("score"))
pdb.set_trace()






