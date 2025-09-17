# app.py

from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from io import StringIO

app = Flask(__name__)

# Tumhara diya gaya dataset ek string ke roop mein
dataset_csv_string = """
id,first_name,last_name,email,gender,part_time_job,absence_days,extracurricular_activities,weekly_self_study_hours,career_aspiration,math_score,history_score,physics_score,chemistry_score,biology_score,english_score,geography_score
1,Paul,Casey,paul.casey.1@gslingacademy.com,male,False,3,False,27,Lawyer,73,81,93,97,63,80,87
2,Danielle,Sandoval,danielle.sandoval.2@gslingacademy.com,female,False,2,False,47,Doctor,90,86,96,100,90,88,90
3,Tina,Andrews,tina.andrews.3@gslingacademy.com,female,False,9,True,13,Government Officer,81,97,95,96,65,77,94
4,Tara,Clark,tara.clark.4@gslingacademy.com,female,False,5,False,3,Artist,71,74,88,80,89,63,86
5,Anthony,Campos,anthony.campos.5@gslingacademy.com,male,False,5,False,10,Unknown,84,77,65,65,80,74,76
6,Kelly,Wade,kelly.wade.6@gslingacademy.com,female,False,2,False,26,Unknown,93,100,67,78,72,80,84
7,Anthony,Smith,anthony.smith.7@gslingacademy.com,male,False,3,True,23,Software Engineer,99,96,97,73,88,76,64
8,George,Short,george.short.8@gslingacademy.com,male,True,2,True,34,Software Engineer,95,95,82,63,84,70,85
9,Stanley,Gutierrez,stanley.gutierrez.9@gslingacademy.com,male,False,6,False,25,Unknown,94,68,94,85,81,74,72
10,Audrey,Simpson,audrey.simpson.10@gslingacademy.com,female,False,3,True,18,Teacher,98,69,88,71,67,71,73
... (rest of your data) ...
"""

# Pandas ki madad se dataset ko load karein
df = pd.read_csv(StringIO(dataset_csv_string))

# Data ko saaf aur prepare karein
df = df.dropna()
df['gender'] = df['gender'].map({'male': 0, 'female': 1})
df['part_time_job'] = df['part_time_job'].astype(int)
df['extracurricular_activities'] = df['extracurricular_activities'].astype(int)

# 'career_aspiration' ko numbers mein badalne ke liye LabelEncoder ka upyog
le = LabelEncoder()
df['career_aspiration_numeric'] = le.fit_transform(df['career_aspiration'])

# Features aur target columns ko define karein
features_columns = [
    'gender', 'part_time_job', 'absence_days', 
    'extracurricular_activities', 'weekly_self_study_hours',
    'math_score', 'history_score', 'physics_score', 'chemistry_score',
    'biology_score', 'english_score', 'geography_score'
]

X = df[features_columns]
y = df['career_aspiration_numeric']

# Model ko train karein
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Web server ke routes ko define karein
@app.route('/')
def home():
    # Jab user homepage par aayega, to index.html dikhayega
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Jab user form submit karega, to yeh function chalega
    try:
        user_input = request.form.to_dict()
        user_input['gender'] = int(user_input['gender'])
        user_input['part_time_job'] = int(user_input['part_time_job'])
        user_input['extracurricular_activities'] = int(user_input['extracurricular_activities'])
        
        for col in ['absence_days', 'weekly_self_study_hours', 'math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score']:
            user_input[col] = int(user_input[col])

        user_data = pd.DataFrame([user_input])
        
        predicted_numeric = model.predict(user_data)
        predicted_career = le.inverse_transform(predicted_numeric)[0]
        
        return render_template('index.html', prediction_text=f"Aapke liye sabse achha career hai: {predicted_career} 🚀")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)