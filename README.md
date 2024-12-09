# redbus-
Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

import streamlit as st
import pandas as pd
import mysql.connector

 

# Map state names to their corresponding file paths
file_paths = {
    "Kerala": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_KR.csv",
    "Kadamba": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_KT.csv",
    "West Bengal": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_WB.csv",
    "Bihar": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_BH.csv",
    "Assam": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_AS.csv",
    "Himachal": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_HP.csv",
    "Chandigarh": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_CH.csv",
    "Jammu": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_JK.csv",
    "Telangana": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_TG.csv",
    "Uttar Pradesh": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_UP.csv",
}

# States Page
def states_page():
    st.header("🏙️ Bus Routes by States")

    # Dropdown for state selection
    selected_state = st.selectbox("Select a State", list(file_paths.keys()))

    # Fare range selection
    fare_range = st.selectbox("Choose Bus Fare Range", ["100-1000", "1000-2000", "2000 and above"])

    # Display routes for the selected state
    if selected_state:
        file_path = file_paths[selected_state]
        st.write(f"Routes for {selected_state}:")
        try:
            #Read routes from CSV
            df = pd.read_csv(file_path)
            routes = df.iloc[:, 0].tolist()  # Assuming the first column contains route names 
            st.selectbox(f"Select a Route in {selected_state}", routes)  

        except Exception as e:
            st.error(f"Error loading routes for {selected_state}: {e}")
        
      
        try:
        
             # Database connection
            mydb = mysql.connector.connect(
                 host="localhost",
                 user="root",
                 password="",
                 database="project_one"
             )

            print(mydb)
            mycursor = mydb.cursor()
            if fare_range == "100-1000":
                 query = f'''SELECT * FROM bus_routes
                              WHERE price BETWEEN 100 AND 1000 AND route_name = '{routes}'
                              ORDER BY price DESC'''
            elif fare_range == "1000-2000":
                 query = f'''SELECT * FROM bus_routes
                              WHERE price BETWEEN 1000 AND 2000 AND route_name = '{routes}'
                              ORDER BY price DESC'''
            else:  # 2000 and above
                 query = f'''SELECT * FROM bus_routes
                              WHERE price > 2000 AND route_name = '{routes}'
                              ORDER BY price DESC'''
            mycursor.execute(query)
            print(mycursor.fetchall())
            result = mycursor.fetchall()
            if result:
                 df = pd.DataFrame(result, columns=[
                     "ID", "route_name", "route_link", "bus_name", "bus_type",
                     "departing_time", "duration", "reaching_time", "star_rating",
                     "price", "seat_availability"
                 ])
                 st.dataframe(df)
            else:
                 st.warning(f"No routes found for {routes} in the selected fare range.")
        except mysql.connector.Error as err:
            print("Error:", e)
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
                print("MySQL connection is closed")        
           
def home_page():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-title {
            font-size: 48px;
            color: #FF5733;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 24px;
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .feature-box {
            background-color: #F0F0F0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .feature-box:hover {
            transform: scale(1.05);
        }
        .feature-icon {
            font-size: 48px;
            color: #FF5733;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.markdown('<div class="main-title">Love for Bus,RedBus!<img src="https://s3.rdbuz.com/Images/rdc/rdc-redbus-logo.webp" alt="RedBus Logo" style="height: 75px; vertical-align: middle; margin-left: 10px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Journey! our Comfort!!</div>', unsafe_allow_html=True)

    # Features Section
    st.header("🌟 Why Choose RedBus?")
    feature_cols = st.columns(4)

    features = [
        ("🛋️", "Comfortable Seats", "Premium seating with extra legroom"),
        ("💺", "Seat Selection", "Choose your preferred seat"),
        ("🏷️", "Best Prices", "Competitive pricing and discounts"),
        ("🔒", "Secure Booking", "Safe and encrypted transactions")
    ]

    for col, (icon, title, description) in zip(feature_cols, features):
        with col:
            st.markdown(f'''
            <div class="feature-box">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            ''', unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="RedBus - Your Journey, Your Way",
    page_icon="c:/Users/Haritha Sree D/Downloads/rdc-redbus-logo.webp",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("REDBUS")
page = st.sidebar.radio("Go to", ["📃 Home", "🔎 Search Buses"])

# Page Selection
if page == "📃 Home":
    home_page()
elif page == "🔎Search Buses":
    states_page()
