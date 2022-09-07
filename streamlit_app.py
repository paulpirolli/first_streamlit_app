import streamlit as st
import pandas as pnd
import requests as req

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

fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + "kiwi")

# clean up json 
fruityvice_normalized = pnd.json_normalize(fruityvice_response.json())
# display
st.dataframe(fruityvice_normalized)