# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

import requests

st.title("✅ App loaded")
st.write("If you can see this, Streamlit is running.")

try:
    cnx = st.connection("snowflake")
    st.success("✅ Snowflake connection object created")

    session = cnx.session()
    st.success("✅ Snowflake session created")

    # Check table exists and has rows
    fruit_table = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    fruit_count = fruit_table.count()
    st.write("🍓 Fruit table row count:", fruit_count)

    # Pull fruit names into a Python list
    fruit_rows = fruit_table.select(col("FRUIT_NAME")).collect()
    fruit_list = [r["FRUIT_NAME"] for r in fruit_rows]
    st.write("🍍 First 5 fruits:", fruit_list[:5])

    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:",
        fruit_list,
        max_selections=5
    )

    st.write("✅ Selected:", ingredients_list)

except Exception as e:
    st.error("❌ Something failed before the dropdown loaded.")
    st.exception(e)
  
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

fruit_rows = my_dataframe.collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_rows]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
    )



if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")




