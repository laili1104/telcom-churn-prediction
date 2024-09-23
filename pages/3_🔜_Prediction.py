import pickle #pip install scikit-learn
import streamlit as st
import pandas as pd
model_file = 'model_C=1.0.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

def main():
	add_selectbox = st.sidebar.selectbox(
	"How would you like to predict?",
	("Online", "Batch"))
	st.title(":soon: Customer Churn Prediction")
	st.markdown("##")
	
	if add_selectbox == 'Online':
		gender = st.selectbox('**Gender :**', ['male', 'female'])
		seniorcitizen= st.selectbox('**Customer is a senior citizen :**', [0, 1])
		partner= st.selectbox('**Customer has a partner :**', ['yes', 'no'])
		dependents = st.selectbox('**Customer has  dependents :**', ['yes', 'no'])
		phoneservice = st.selectbox('**Customer has phone service :**', ['yes', 'no'])
		multiplelines = st.selectbox('**Customer has multiple lines :**', ['yes', 'no', 'no_phone_service'])
		internetservice= st.selectbox('**Customer has internet service :**', ['dsl', 'no', 'fiber_optic'])
		onlinesecurity= st.selectbox('**Customer has online security :**', ['yes', 'no', 'no_internet_service'])
		onlinebackup = st.selectbox('**Customer has online backup :**', ['yes', 'no', 'no_internet_service'])
		deviceprotection = st.selectbox('**Customer has device protection :**', ['yes', 'no', 'no_internet_service'])
		techsupport = st.selectbox('**Customer has tech support :**', ['yes', 'no', 'no_internet_service'])
		streamingtv = st.selectbox('**Customer has streaming TV :**', ['yes', 'no', 'no_internet_service'])
		streamingmovies = st.selectbox('**Customer has streaming movies :**', ['yes', 'no', 'no_internet_service'])
		contract= st.selectbox('**Customer has a contract :**', ['month-to-month', 'one_year', 'two_year'])
		paperlessbilling = st.selectbox('**Customer has a paperless billing :**', ['yes', 'no'])
		paymentmethod= st.selectbox('**Payment option :**', ['bank_transfer_(automatic)', 'credit_card_(automatic)', 'electronic_check' ,'mailed_check'])
		tenure = st.number_input('**Number of months the customer has been with the current telco provider :**', min_value=0, max_value=240, value=0)
		monthlycharges= st.number_input('**Monthly charges :**', min_value=0, max_value=240, value=0)
		totalcharges = tenure*monthlycharges
		output= ""
		output_prob = ""
		input_dict={
				"gender":gender ,
				"seniorcitizen": seniorcitizen,
				"partner": partner,
				"dependents": dependents,
				"phoneservice": phoneservice,
				"multiplelines": multiplelines,
				"internetservice": internetservice,
				"onlinesecurity": onlinesecurity,
				"onlinebackup": onlinebackup,
				"deviceprotection": deviceprotection,
				"techsupport": techsupport,
				"streamingtv": streamingtv,
				"streamingmovies": streamingmovies,
				"contract": contract,
				"paperlessbilling": paperlessbilling,
				"paymentmethod": paymentmethod,
				"tenure": tenure,
				"monthlycharges": monthlycharges,
				"totalcharges": totalcharges
			}

		if st.button("Predict"):
			X = dv.transform([input_dict])
			y_pred = model.predict_proba(X)[0, 1]
			churn = y_pred >= 0.5
			output_prob = float(y_pred)
			output = bool(churn)
		st.success('Churn: {0}, Risk Score: {1}'.format(output, output_prob))
	if add_selectbox == 'Batch':
		file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
		if file_upload is not None:
			# Read the uploaded CSV file
			data = pd.read_csv(file_upload)
			
			# Convert DataFrame to a list of dictionaries
			records = data.to_dict(orient='records')

			# Convert all values to strings
			for record in records:
				for key in record:
					record[key] = str(record[key])

			# Transform the data using DictVectorizer
			X = dv.transform(records)  # Pass the list of dictionaries directly
			
			# Make predictions
			y_pred = model.predict_proba(X)[:, 1]  # Get probabilities for churn class
			
			# Determine if churn occurs based on threshold
			churn = y_pred >= 0.5
			
			# Display the results
			for i, is_churn in enumerate(churn):
				st.write(f"Record {i + 1}: {'Churn' if is_churn else 'No Churn'}")


if __name__ == '__main__':
	main()