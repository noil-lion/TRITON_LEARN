import pickle


file=open("./dataset_properties.pkl","rb")
data=pickle.load(file)
print(data)
file.close()