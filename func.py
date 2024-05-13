from thefuzz import fuzz
from thefuzz import process
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import LabelEncoder
class DiseasePredictor:
    def __init__(self):
        self.df1 = pd.read_csv("FinalSymptoms.csv")
        label_encoder = LabelEncoder()
        self.df2 = pd.DataFrame()
        self.df2["Symtoms"] = self.df1['Symptoms']
        self.df1['Symptoms'] = label_encoder.fit_transform(self.df1['Symptoms'])
        self.df2["Encoded"] = self.df1['Symptoms'] 
        correlation_matrix = self.df1.corr()
        self.target_correlations = correlation_matrix['Symptoms'].sort_values(ascending=False)
        self.imp_c =  list(self.target_correlations.index)
        self.imp_c.remove("Symptoms")

    def predict(self,text:str):
        values = process.extract(text,self.imp_c,limit=len(self.target_correlations))
        df = pd.DataFrame(columns=self.target_correlations.index)
        df.loc[0] = np.zeros(len(self.target_correlations))
        for i  in values:
            if(i[1]>85):
                df.loc[0][i[0]] = 1
        S = pd.DataFrame(columns=["Symptom","Relation"])
        for i in range(len(self.df1)):
            S.loc[len(S)] = [self.df2.iloc[self.df2.index[self.df2['Encoded'] == self.df1.loc[i]["Symptoms"]]]["Symtoms"][i],df.corrwith(self.df1.iloc[i], axis=1)[0]]
        S = S.sort_values("Relation",ascending=False)
        print(S)
        out:list = list()
        res = pd.DataFrame(columns=["Disease","Percentage"])
        for i in range(0,10):
            item = S.iloc[i+5]
            item2 = S.iloc[i]
            sym = str(item["Symptom"])
            sym = sym.replace("_"," ")
            sym = sym.capitalize()
            realtion = item2["Relation"]
            res.loc[i,"Disease"] = sym
            res.loc[i,"Percentage"] = str(abs(realtion*100))[:4]+"%"
        return res
        

