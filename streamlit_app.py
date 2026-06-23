# Import python packages
import streamlit as st

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
# getting a text input for the name
name_on_order = st.text_input("Your Beautiful Name: ")
# displaying a name in the bottom afer user types it
st.write("The Name For Your Order:", name_on_order)


cnx = st.connection("snowflake")
# connecting to snowflake environment
session = cnx.session()
# connecting to fruit option table and making fruit name the options
# we are assigning my_dataframe the fruit_name table
my_dataframe = session.table("smoothies.public.fruit_options"). select(col("FRUIT_NAME"))

#creating the dropdown visual and assigning ingredients_list variable for that dropdown to store the information
ingredients_list = st.multiselect("Choose Up To 5 Ingredients", my_dataframe, max_selections = 5 )

# when atleast one item is selected run this code
if ingredients_list:
    # we are creating a variable which is empty
    ingredients_string = ''
    # for each fruit picked by the user, it adds blank space after it.
    # it saves that information into ingredients_string
    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '

    # creating a SQL statement which we will use to enter data/options into a table
    # we will insert the data into orders table into ingredients column
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # adding a submit button and we are saving the action into a variable
    # the time_to_insert becomes true if when clicked, or else it stays false
    time_to_insert = st.button ('Submit Order')

    # if the button is clicked
    if time_to_insert:
        # run the query into snoflake, the query which we designed earlier
        session.sql(my_insert_stmt).collect()

        # once submitted, it notifies the user
        st.success ("✅" + 'Your Smoothie Is Ordered, ' + name_on_order +"!")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json())
