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

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pnd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else:
        back_from_fuction = get_fruityvice_data(fruit_choice)
        # display
        st.dataframe(back_from_fuction)
except err as e:
    st.error()


st.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

#add a button to load the fruit
if st.button('Get Fruit Load List'):
    my_cnx = snfkcn.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows)


# new section for adding fruit
#allow the end user to add a row to the DB
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
    my_cnx = snfkcn.connect(**st.secrets["snowflake"])
    back_from_fuction = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    st.text(back_from_fuction)
