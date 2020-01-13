import csv
import numpy as np
from utils import *
from dummy_user import get_dummy_user
from infer_user import infer_user

def user_job_requirements(user, target_job):
	code = job_to_code(target_job)
	
	jid = get_jobs().index(code)
	attributes = get_attributes();
	ja = get_ja_matrix()
	target_user = { a:ja[jid, i] for i, a in enumerate(attributes) };
	
	skill_diff = {a:target_user[a] - user[a] for a in user}
	return [ (a, skill_diff[a]) for a in sorted(skill_diff, key=skill_diff.get, reverse=True) ]

if __name__ == "__main__":
	##dummy user
	dummy="Choreographers"
	du = get_dummy_user(dummy) 
	user = infer_user(du)
	
	target_job = "Computer Network Architects"
	print("For the dummy user (", dummy, ") to fit the target job (", target_job, ")")
	print("The top 5 skills are:")
	for s in user_job_requirements(user, target_job)[:5]:
		print(s)

