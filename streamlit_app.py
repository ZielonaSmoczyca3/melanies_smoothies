# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col as col

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose your prefered fruits for your 
  **SMOOTHIE** check
  our webiste for ordering
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

# to comment a block CTRL+/
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Orange", "Kiwi"),
# )
# st.write("You selected:", option)

name_on_order = st.text_input('Personalise your smoothie and choose a name for your drink:')
st.write('The label on your smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 fruits: ', my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    submit_order = st.button('Submit Your Order')
    if submit_order:
    #if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered for: ' + '' + name_on_order + '',  icon="✅")


import requests
smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/apple")
st.text(smoothiefroot_response.json())
