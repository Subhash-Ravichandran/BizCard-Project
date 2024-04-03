
import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
from streamlit_option_menu import option_menu
import sqlite3
import shutil
import os
import random

def image_to_text(path):

  #opening Image
  input_image=Image.open(path)

  #image to array
  image_array=np.array(input_image)

  #Data Extrction Using OCR
  reader=easyocr.Reader(['en'])
  text=reader.readtext(image_array,detail=0)

  return text, input_image


def extracted_text(texts):
  extr_dict={"Name":[],"Designation":[],"Company_Name":[], "Contact":[], "E_Mail":[],"Website":[],"Address":[],"Pincode":[]}
  extr_dict["Name"].append(texts[0])
  extr_dict["Designation"].append(texts[1])
  for i in range(2,len(texts)):
    if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):
      extr_dict["Contact"].append(texts[i])

    elif "@" in texts[i] and ".com" in texts[i]:
      extr_dict["E_Mail"].append(texts[i])

    elif "www" in texts[i] or "WWW" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]  or ".com" in texts[i] :
      small=texts[i].lower()
      extr_dict["Website"].append(small)

    elif "TamilNadu" in texts[i] or "Tamil Nadu" in texts[i] or texts[i].isdigit():
      extr_dict["Pincode"].append(texts[i])

    elif re.match(r'^[A-Za-z]',texts[i]):
      extr_dict["Company_Name"].append(texts[i])

    else:
      remove_colon= re.sub(r'[,;]', "",texts[i])
      extr_dict["Address"].append(remove_colon)

  for key,value in extr_dict.items ():
    if len(value)>0:
      concatenate=" ".join(value)
      extr_dict[key]=[concatenate]
    else:
      value ="NA"
      extr_dict[key]=[value]

  return extr_dict



#Streamlit Code

st.set_page_config(layout="wide")
st.markdown(
    f'<h1 style="color: {"#003366"}; text-align: center;">Extracting Business Card Data with OCR</h1>',
    unsafe_allow_html=True)
st.markdown(f""" <style>.stApp {{
                        background:url("https://i.pinimg.com/originals/e5/4e/2e/e54e2ef0a33bbab5be4c0b199d03b786.jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)

#with st.sidebar:
select = option_menu(
    menu_title = None,
    options = ["Home","Upload & Modify","Delete"],
    icons =["house","upload","trash"],
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background": "#4682B4","size":"cover", "width": "150"},
        "icon": {"color": "white", "font-size": "20px"},

        "nav-link": {"font-size": "20px", "text-align": "center", "--hover-color": "#87CEEB"},
        "nav-link-selected": {"background-color": "#4682B4"}})


if select =="Home":
  # col1,col2=st.columns(2)
  # with col1:
  col1, col2, col3 = st.columns([1, 2, 1])  # Creating columns to center align the image
  with col2:
    st.image("https://miro.medium.com/v2/resize:fit:1400/0*V7NS3dvYQLVi6DFL.gif", width=500)
# with col2:
  st.markdown(f'<h1 style="color: {"#000080"};">Technologies Used:</h1>',unsafe_allow_html=True)
  st.write(f'<p style="font-size: {"24px"};color: {"#0000CD"};">OCR, Streamlit GUI, SQL, Data Extraction</p>',unsafe_allow_html=True)

  st.markdown(f'<h1 style="color: {"#000080"};">Description:</h1>',unsafe_allow_html=True)
  st.write(f'<p style="font-size: {"24px"};color: {"#0000CD"};">"BizCardX" is an advanced tool utilizing OCR technology to swiftly extract crucial data from business cards. With seamless integration and user-friendly interface, it streamlines contact information retrieval, optimizing productivity and organization for professionals.</p>',unsafe_allow_html=True)

elif select == "Upload & Modify":
  img= st.file_uploader("Upload the Image", type = ["png","jpg","jpeg"])

  if img is not None:
    st.image(img,width = 500)

    text_image, input_img= image_to_text(img)

    text_dict = extracted_text(text_image)

    if text_dict:
      st.success("Text is Extracted Successfully")

    df=pd.DataFrame(text_dict)

    #converting image to bytes

    Image_bytes= io.BytesIO()
    input_img.save(Image_bytes, format = "PNG")

    image_data=Image_bytes.getvalue()

    #creating Dictionary
    data = {"IMAGE":[image_data]}

    df_1= pd.DataFrame(data)

    concat_df=pd.concat([df,df_1],axis = 1)

    st.dataframe(concat_df)

    button=st.button("Load",use_container_width = True)
    if button:
      #Data Base connection
      mydb = sqlite3.connect('Biz.db')
      cursor = mydb.cursor()

      # Table Creation

      create_table_query = '''CREATE TABLE IF NOT EXISTS biz_card
                        (Name varchar(225),
                        Designation varchar(50),
                        Company_Name varchar(225),
                        Contact varchar(225),
                        E_Mail varchar(225),
                        Website text,
                        Address text,
                        Pincode varchar(225),
                        image text )'''

      cursor.execute(create_table_query)
      mydb.commit()

      insert_query = '''INSERT INTO biz_card(Name,Designation,Company_Name,Contact,E_Mail,
                    Website,Address,Pincode,image)

                    values(?,?,?,?,?,?,?,?,?)'''

      datas = concat_df.values.tolist()[0]
      cursor.execute(insert_query,datas)
      mydb.commit()

      st.success("SAVED SUCCESSFULLY")

  method=st.radio("Select the method",["Preview","Modify"],horizontal=True)

  if method == "Preview":
    mydb = sqlite3.connect('Biz.db')
    cursor = mydb.cursor()

    #select query
    select_query="select * from biz_card"

    cursor.execute(select_query)
    table=cursor.fetchall()
    mydb.commit()

    table_df=pd.DataFrame(table, columns=("Name","Designation", "Company_Name", "Contact", "E-mail", "website", "Address", "Pincode", "Image"))
    st.dataframe(table_df)

  elif method == "Modify":
    mydb = sqlite3.connect('Biz.db')
    cursor = mydb.cursor()

    #select query
    select_query="select * from biz_card"

    cursor.execute(select_query)
    table=cursor.fetchall()
    mydb.commit()

    table_df=pd.DataFrame(table, columns=("Name","Designation", "Company_Name", "Contact",
                                         "E-mail", "website", "Address", "Pincode", "Image"))

    col1,col2 = st.columns(2)
    with col1:

      selected_name=st.selectbox("Select the Name",table_df["Name"])

    df_3 = table_df[table_df["Name"] == selected_name]

    df_4=df_3.copy()


    col1,col2 = st.columns(2)
    with col1:
      mo_name = st.text_input("Name",df_3["Name"].unique()[0])
      mo_desi = st.text_input("Designation",df_3["Designation"].unique()[0])
      mo_comp = st.text_input("Company_Name",df_3["Company_Name"].unique()[0])
      mo_cont = st.text_input("Contact",df_3["Contact"].unique()[0])
      mo_email = st.text_input("E-mail",df_3["E-mail"].unique()[0])

      df_4["Name"] = mo_name
      df_4["Designation"] = mo_desi
      df_4["Company_Name"] = mo_comp
      df_4["Contact"] = mo_cont
      df_4["E-mail"] = mo_email

    with col2:

      mo_web = st.text_input("website",df_3["website"].unique()[0])
      mo_addr = st.text_input("Address",df_3["Address"].unique()[0])
      mo_pin = st.text_input("Pincode",df_3["Pincode"].unique()[0])
      mo_img = st.text_input("Image",df_3["Image"].unique()[0])

      df_4["website"] = mo_web
      df_4["Address"] = mo_addr
      df_4["Pincode"] = mo_pin
      df_4["Image"] = mo_img

    st.dataframe(df_4)

    col1,col2=st.columns(2)
    with col1:
      button_3 = st.button("Modify", use_container_width = True)

    if button_3:
      mydb = sqlite3.connect('Biz.db')
      cursor = mydb.cursor()

      cursor.execute(f"Delete from biz_card where Name = '{selected_name}'")
      mydb.commit()

      insert_query = '''INSERT INTO biz_card(Name,Designation,Company_Name,Contact,E_Mail,
                    Website,Address,Pincode,image)

                    values(?,?,?,?,?,?,?,?,?)'''

      datas = df_4.values.tolist()[0]
      cursor.execute(insert_query,datas)
      mydb.commit()

      st.success("MODIFIED SUCCESSFULLY")





elif select == "Delete":

  mydb = sqlite3.connect('Biz.db')
  cursor = mydb.cursor()

  col1,col2=st.columns(2)
  with col1:

    select_query = "SELECT Name FROM biz_card"

    cursor.execute(select_query)
    table1=cursor.fetchall()
    mydb.commit()

    names = []

    for i in table1:
      names.append(i[0])

    name_select = st.selectbox("select the name", names)

  with col2:
    select_query_1=f"select Designation from biz_card where name = '{name_select}'"

    cursor.execute(select_query_1)
    table2=cursor.fetchall()
    mydb.commit()

    designations = []

    for j in table2:
      designations.append(j[0])

    desi_select = st.selectbox("select the designation",options = designations)

  if name_select and desi_select:
    col1,col2,col3=st.columns(3)

    with col1:
      st.write(f"Selected Name : {name_select}")
      st.write("")
      st.write("")
      st.write("")
      st.write(f"selected designation : {desi_select}")

    with col2:
      st.write("")
      st.write("")
      st.write("")
      st.write("")

      remove = st.button("Delete",use_container_width=True)

      if remove:
        cursor.execute(f"Delete From biz_card where Name = '{name_select}' and designation = '{desi_select}'")
        mydb.commit()

        st.warning("Deleted")





































