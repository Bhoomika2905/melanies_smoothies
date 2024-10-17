# Import python packages
from snowflake.snowpark.functions import col
import streamlit as st
cnx=st.connection("snowflake")
session=cnx.session();

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


#option = st.selectbox(
#    "How would you like to be contacted?",
#    ("Strawberries", "Banana", "Peaches"),
#)
#st.write("You selected:", option)



my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie")
st.write("""The name on your Smoothie will be: """ + name_on_order)

ingredients_list = st.multiselect(
    'Choose Upto 5 Ingredients: ',my_dataframe,max_selections=5
)
if len(ingredients_list) == 5:
    st.warning("You've reached the maximum of 5 ingredients.")
               
ingredient_string=''
if ingredients_list:
    for ingredient in ingredients_list:
        ingredient_string=ingredient_string+"\t"+ingredient
    st.write(ingredient_string)
else:
    st.write("No Ingredients Chosen!")

my_insert_stmt1 = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','"""+name_on_order+"""')"""

#st.write(my_insert_stmt)
time_to_insert1=st.button('SUBMIT')

#new section to display fruityvise nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

import requests
import streamlit as st

# Fetch data from Fruityvice API
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df=st.dataframe(data=fruityvice_response.JSON(),use_container_width=True)


if time_to_insert1:
    session.sql(my_insert_stmt1).collect()
    st.success(f'Your Smoothie is Ordered, {name_on_order}!', icon="✅")
