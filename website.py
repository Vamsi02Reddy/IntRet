# import streamlit as st
# import pickle
# import numpy as np
# model = pickle.load(open('model.pkl','rb'))

# def predictSalary(salary):
#     x = int(salary)
#     prediction = model.predict([[x]])
#     return prediction[0]

# def main():
#     st.title("Linear model testing")
#     xp = st.text_input("Enter YearsExperience")

#     if st.button("Predict"):
#         output = predictSalary(xp)
#         st.success(output)

# if __name__ == '__main__':
#     main()

import streamlit as st
import pandas as pd
import scikit-learn
import numpy as np
import pickle
import math
pickled_model = pickle.load(open('model.pkl', 'rb'))


df = pd.read_csv("./dataset.csv")
df["Symptoms"] = 0
records = df.shape[0]


for i in range(records):
    values = df.iloc[i].values
    
    values = values.tolist()
    # print(values)
    if 0 in values:
        df["Symptoms"][i] = values[1:values.index(0)]
    else:
        df["Symptoms"][i] = values[1:]

column_values = df[['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
       'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
       'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
       'Symptom_15', 'Symptom_16', 'Symptom_17']].values.ravel()


symps = pd.unique(column_values)
symps = symps.tolist()
symps = [i for i in symps if str(i) != "nan"]


symptoms = pd.DataFrame(columns = symps,index = df.index)

symptom_index = {}
for index, value in enumerate(symptoms):
#     symptom = "".join([i for i in value.split("_")])
    symptom = value
    symptom_index[symptom] = index

data_dict = {
    "symptom_index": symptom_index,
}
df_new = pd.DataFrame(columns = symps,index = df.index)
df_new = df_new.drop(range(1,records))

col_names = (list(df_new))

def predictDisease(symptoms):

    # print(symptoms)
    for i in col_names:
        if i in symptoms:
            df_new[i] = 1
        else:
            df_new[i] = 0
    return (pickled_model.predict(df_new))

    
    


# symptoms["Symptoms"] = df["Symptoms"]
# for i in symps:
#     symptoms[i] = symptoms.apply(lambda x:1 if i in x.Symptoms else 0, axis=1)

# symptoms["Disease"] = df["Disease"]
# symptoms = symptoms.drop("Symptoms",axis=1)

# testingDf = symptoms.drop("Disease",axis=1)
# print(testingDf)

number = st.text_input("Enter number of symptoms")
try:
    number = int(number)
except:
    number = 0
selected_options = []
if(number<=8):
    for i in range(number):
        option = st.selectbox('Symptom',list(symptoms.columns),key=i)
        'You selected: ', option
        selected_options.append(option)
else:
    st.write("Cant enter more than 8 symptoms")
# option1 = st.selectbox('Symptom 2',list(symptoms.columns),key=2)
# 'You selected: ', option1
# option2= st.selectbox('Symptom 3',list(symptoms.columns),key=3)
# 'You selected: ', option2
# option3= st.selectbox('Symptom 4',list(symptoms.columns),key=4)
# 'You selected: ', option3


# selected_options = [option,option1,option2,option3]
# print(selected_options)
def tellDescription(disease):
    df_description = pd.read_csv('./symptom_Description.csv')
    description = df_description[df_description["Disease"]==disease]["Description"].values[0]
    # print(description)
    return description

precautions = []

def tellPrecautions(disease):
    df_precautions = pd.read_csv('./symptom_precaution.csv')
    precaution1 = df_precautions[df_precautions["Disease"]==disease]["Precaution_1"].values[0]
    precaution2 = df_precautions[df_precautions["Disease"]==disease]["Precaution_2"].values[0]
    precaution3 = df_precautions[df_precautions["Disease"]==disease]["Precaution_3"].values[0]
    precaution4 = df_precautions[df_precautions["Disease"]==disease]["Precaution_4"].values[0]
    precautions.append(precaution1)
    precautions.append(precaution2)
    precautions.append(precaution3)
    precautions.append(precaution4)

    # print(precautions)
    return precautions
if(number>0 and number<8):
    if st.button("Predict"):
        "Predicted Disease is: ", predictDisease(selected_options)[0]
        st.write(tellDescription(predictDisease(selected_options)[0]))
        prec = (tellPrecautions(predictDisease(selected_options)[0]))
        "Precautions:"
        for i in prec:
            try:
                if math.isnan(i):
                    continue
                
            except:
                st.write("*",i)
        # "1. ", prec[0]
        # "2. ", prec[1]
        # "3. ", prec[2]
        # "4. ", prec[3]
