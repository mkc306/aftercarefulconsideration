import textract
from textblob import TextBlob
import pdb
import os 

JOB_SPECS = ['2019_JobSpec_AutomationLead.docx', '2019_JobSpec_SRE.docx', '2019_JobSpec_InfraMgr.docx', '2019_JobSpec_Oracle.docx']
with open('skills.txt') as f:
	skills = f.read().split('\n')

skills = [s.lower() for s in skills]

#results = []
job_requirements = [textract.process(j).decode('utf8') for j in JOB_SPECS]
keywords = dict()
for i in range(len(job_requirements)):
	#match_dict = {JOB_SPECS[i]:matches}
	matches = []
	#pdb.set_trace()
	for word in job_requirements[i].strip().split(" "):
		word = word.lower()
		if word in skills: matches.append(word.lower()) #slow as skills very large 
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
		scores.append({resumes[i]:score})
	results[job_name] = scores
#print reuslts in descending order 
pdb.set_trace()







# y =j.split('.')
# #y = spacy.explain("obj")
# #pdb.set_trace()
#blob = TextBlob(x)
# #print(blob.tags)

# for d in y:
# 	d = TextBlob(d)
# 	print(d.tags)

