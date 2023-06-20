import pandas as pd
from datetime import datetime
import math

# Functions definitions for conversion
def convert_gender(gender: str) -> str:
    gender = gender.replace("string_", "")
    gender = gender.replace("boolean_", "")
    gender = gender.replace("character_", "")

    gender_mappings = {'0': 'Male', '1': 'Female', 'F': 'Female', 'M': 'Male'}

    if gender in gender_mappings:
        gender = gender_mappings[gender]

    return gender

def convert_name(name):
    if isinstance(name, float) and math.isnan(name):  
        return ""

    if isinstance(name, str):
        name = name.replace("string_", "")
        name = name.replace("\\", "")
        name = name.replace('"', '')
        name = name.capitalize()
    return name
    
def convert_email(email):
    if isinstance(email, str):
        email = email.replace("string_", "")
        email = email.lower()
    return email

def convert_city(city):
    if isinstance(city, str):
        city = city.replace("string_", "")
        city = city.replace("-", " ")
        city = city.replace("_", " ")
        city = city.title()
    return city

def convert_age(age: str) -> str:
    age = str(age)
    age = ''.join(filter(str.isdigit, age))
    return age

   
def my_m_and_a(csv1, csv2, csv3):
    # Read the CSV contents into pandas DataFrames
    df1 = pd.read_csv(csv1)
    # Perform operations on the DataFrames
    df1['Gender'] = df1['Gender'].apply(convert_gender)
    df1['FirstName'] = df1['FirstName'].apply(convert_name)
    df1['LastName'] = df1['LastName'].apply(convert_name)
    df1['Email'] = df1['Email'].apply(convert_email)
    df1['City'] = df1['City'].apply(convert_city)
    df1['Country'] = "U.S.A"
    df1['created_at'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    
    df2 = pd.read_csv(csv2, names=['Age', 'City', 'Gender', 'Name', 'Email'], header=None, sep= ";")
    # Perform operations on the DataFrames
    df2['Gender'] = df2['Gender'].apply(convert_gender)
    df2['FirstName'] = df2['Name'].apply(lambda x: convert_name(x.split(' ')[0]))
    df2['LastName'] = df2['Name'].apply(lambda x: convert_name(x.split(' ')[1]))
    df2['Email'] = df2['Email'].apply(convert_email)
    df2['Age'] = df2['Age'].apply(convert_age)
    df2['City'] = df2['City'].apply(convert_city)
    df2['Country'] = "U.S.A"
    df2 = df2.drop('Name', axis=1)
    df2['created_at'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    
    df3 = pd.read_csv(csv3, sep='\t', names=['Gender', 'Name', 'Email', 'Age', 'City', 'Country'], skiprows=1)
    # Perform operations on the DataFrames
    df3['Gender'] = df3['Gender'].apply(convert_gender)
    df3['FirstName'] = df3['Name'].apply(lambda x: convert_name(x.split(' ')[0]))
    df3['LastName'] = df3['Name'].apply(lambda x: convert_name(x.split(' ')[1]))
    df3['Email'] = df3['Email'].apply(convert_email)
    df3['Age'] = df3['Age'].apply(convert_age)
    df3['City'] = df3['City'].apply(convert_city)
    df3['Country'] = "U.S.A"
    df3 = df3.drop('Name', axis=1)
    df3['created_at'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    

    # Concatenate the three DataFrames
    merged_df = pd.concat([df1, df2, df3], ignore_index=True)  
    # Rename the columns of the merged DataFrame
    merged_df = merged_df.rename(columns={'age': 'Age', 'city':'City', 'firstname': 'FirstName', 'lastname': 'LastName', 'gender':'Gender'})
    merged_df['Age'] = merged_df['Age'].astype("string")
    

    return merged_df
