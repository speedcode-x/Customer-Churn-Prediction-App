import streamlit as st
import numpy as np
import pandas as pd

# Define a key for storing the data in the session state
DATA_KEY = "data_key"

# Set page configuration
st.set_page_config(
    page_title='View Data',
    page_icon='📊',
    layout='wide'
)

# Function to load CSV data
@st.cache_resource
def load_data(file_path):
    return pd.read_csv(file_path)

# Check if the user is authenticated
if not st.session_state.get("authentication_status"):
    st.info('Please log in to access the application from the homepage.')
else:
    # Title of the page
    st.title('Vodafone Data')

    # Load CSV data
    file_path = "data/data.csv"
    data_df = load_data(file_path)

    # Set the data into the session state
    st.session_state[DATA_KEY] = data_df

    # Selectbox to choose the type of features to display
    selected_feature_type = st.selectbox("Select data features", options=['All Features', 'Numerical Features', 'Categorical Features'],
                                         key="selected_columns")

    # Function to select features based on type
    def select_features(feature_type, df):
        if feature_type == 'Numerical Features':
            # Filter numerical features
            numerical_df = df.select_dtypes(include=np.number)
            return numerical_df
        elif feature_type == 'Categorical Features':
            # Filter categorical features
            categorical_df = df.select_dtypes(include='object')
            return categorical_df
        else:
            # Return the entire DataFrame
            return df

    # Display the selected features
    if selected_feature_type == 'All Features':
        # Show all features if selected
        st.write(st.session_state[DATA_KEY])
    else:
        # Show selected type of features
        st.write(select_features(selected_feature_type, st.session_state[DATA_KEY]))
