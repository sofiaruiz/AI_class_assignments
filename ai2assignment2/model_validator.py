import pandas as pd
import pomegranate as pom


exp_csv = "med_ex_exp.csv"
obs_csv = "med_ex_obs.csv"
node_names = ["X","Z","Y","M","W"]

def create_model(csv, node_names):
	data = pd.read_csv(csv)
	model = pom.BayesianNetwork.from_samples(data, state_names=node_names)
	return model


if __name__ == "__main__":
	exp_model = create_model(exp_csv, node_names)
	obs_model = create_model(obs_csv, node_names)


	print("Models created from data")
	print()


	evidence = [{"X":0},{"X":1}]
	exp_model_probs = {}
	obs_model_probs = {}

	for ev in evidence:
		ev_key = list(ev.keys())[0]
		exp_model_probs[ev_key+"="+str(ev[ev_key])] = exp_model.predict_proba(ev)[1].values()[0]
		obs_model_probs[ev_key+"="+str(ev[ev_key])] = obs_model.predict_proba(ev)[1].values()[0]

	print("Experimental Data Probability of Y=1 for do(X)")
	print(exp_model_probs)

	print("Observational Data Probability of Y=1 for do(X)")
	print(obs_model_probs)