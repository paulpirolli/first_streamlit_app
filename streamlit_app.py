import streamlit as st
import pandas as pnd
import requests as req
import snowflake.connector as snfkcn
from urllib.error import URLError as err

my_fruit_list = pnd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

st.title('My Parents\' New Healthy Diner')

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

st.dataframe(fruits_to_show)

# new section for fruityvice advice
st.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else:
        fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # clean up json 
        fruityvice_normalized = pnd.json_normalize(fruityvice_response.json())
        # display
        st.dataframe(fruityvice_normalized)
except err as e:
    st.error()

my_cnx = snfkcn.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)


# new section for adding fruit

add_my_fruit = st.text_input('What fruit would you like to add?','Jackfruit')
st.write('The user entered ', add_my_fruit)