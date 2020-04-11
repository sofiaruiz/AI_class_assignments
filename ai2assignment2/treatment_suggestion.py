from model_validator import create_model
import pandas as pd
import pomegranate as pom

#specify data files and node names
exp_csv = "med_ex_exp.csv"
obs_csv = "med_ex_obs.csv"
node_names = ["X","Z","Y","M","W"]

#create models using method from model_validator
exp_model = create_model(exp_csv, node_names)
obs_model = create_model(obs_csv, node_names)


#create evidence for exp data. want to look at recovery for individuals that are W=0 and M=0 for both X=0 and X=1
exp_evidence = [{"X":0,"W":0,"M":0},{"X":1,"W":0,"M":0}]

#create observational evidence. want to look at rate at which doctors are prescribing each medication for W=0 M=0
obs_evidence = {"W":0,"M":0}


#calculate the recovery rate for both X=0 and X=1 using exp_model with evidence of W=0 M=0
exp_model_probs = {}
for ev in exp_evidence:
	ev_key = list(ev.keys())[0]
	exp_model_probs[ev_key+"="+str(ev[ev_key])] = exp_model.predict_proba(ev)[1].values()[0]

	
#calculate the rate at which doctors are prescribing X=0 and X=1 for patients with W=0 and M=0
obs_model_probs = obs_model.predict_proba(obs_evidence)[0].values()

prescription_rates = {"X=0":obs_model_probs[0],"X=1":obs_model_probs[1]}


#get list of the treatments
treatments = list(exp_model_probs.keys())


#print out results detailing which treatment is more effective for patients with W=0 and M=0 per the experimental data
#and the rate at which doctors are prescribing this treatement method in the wild
print()

if exp_model_probs[treatments[0]] > exp_model_probs[treatments[1]]:
	print(f"Optimal Treatment = {treatments[0]}. {round((exp_model_probs[treatments[0]]-exp_model_probs[treatments[1]])*100,2)}% more optimal than other treatment option.")
	print(f"Doctors in the wild are prescribing this treatment at a rate of {round(prescription_rates[treatments[0]]*100, 2)}%.")
else:
	print(f"Optimal Treatment = {treatments[1]}. {round((exp_model_probs[treatments[1]]-exp_model_probs[treatments[0]])*100,2)}% more optimal than other treatment option.")
	print(f"Doctors in the wild are prescribing this treatment at a rate of {round(prescription_rates[treatments[1]]*100, 2)}%.")

print()