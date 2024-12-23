import streamlit as st
import pandas as pd
import mysql.connector
import pymysql

# Sidebar Navigation
st.sidebar.title("REDBUS")
page = st.sidebar.radio("Go to", ["📃 Home", "🔎 Search Buses"])

if page == "📃 Home":
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
            border-radius: 5px;
            padding: 5px;
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

states_to_files = {
    "Kerala": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_KR.csv",
    "Kadamba": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_KT.csv",
    "West Bengal": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_WB.csv",
    "Bihar": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_BH.csv",
    "Assam": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_AS.csv",
    "Himachal Pradesh": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_HP.csv",
    "Chandigarh": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_CH.csv",
    "Jammu and Kashmir": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_JK.csv",
    "Telangana": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_TG.csv",
    "Uttar Pradesh": "C:/Users/Haritha Sree D/.vscode/project_redbus/scrap/df_UP.csv"
}
if page == "🔎 Search Buses":
    st.title("Bus Routes by States")
    price_range=["100-500","500-1000","1000 and above"]
    states = ["Kerala", "Kadamba", "West Bengal", "Bihar", "Assam", "Himachal Pradesh", "Chandigarh", "Jammu and Kashmir", "Telangana", "Uttar Pradesh"]
    selected_state = st.selectbox("Select a State", states)

    
    if selected_state is not None:
        
        df = pd.read_csv(states_to_files[selected_state])
        route_options = list(df[df.columns[0]])
        selected_route = st.selectbox("Select a Route", route_options)

    
    if selected_route is not None:
        selected_price = st.selectbox("Select a Price Range", price_range)

        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="project_one"
        )
        mycursor = mydb.cursor()

        # Modify the query 
        if selected_price == "100-500":
            price_condition = "price BETWEEN 100 AND 500"
        elif selected_price == "500-1000":
            price_condition = "price BETWEEN 500 AND 1000"
        else:  # "1000 and above"
            price_condition = "price >= 1000"

        # SQL query 
        query = f"""
        SELECT * FROM bus_routes 
        WHERE route_name = %s AND {price_condition}
        """
        
        # Execute the query 
        mycursor.execute(query, (selected_route,))

        # Fetch all the results
        results = mycursor.fetchall()

        # Create DataFrame
        df = pd.DataFrame(results, columns=['ID', 'route_name', 'route_link', 'bus_name', 'bus_type', 
                                            'departing_time', 'duration', 'reaching_time', 'star_rating', 
                                            'price', 'seat_availability']) 
        st.dataframe(df) 
 
                           
