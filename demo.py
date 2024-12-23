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
    
    # Filter options
    price_range = ["100-500", "500-1000", "1000 and above"]
    time_slots = [
    "Morning (06:00-12:00)",
    "Afternoon (12:00-18:00)", 
    "Evening (18:00-24:00)",
    "Night (00:00-06:00)"
      ]
    ratings = ["Any", "3★ & above", "4★ & above"]
    availability =["All",
        "Very Limited (1-5 seats)",
        "Limited (6-10 seats)", 
        "Available (11-20 seats)",
        "Many Available (20+ seats)"
       ]
    
    states = ["Kerala", "Kadamba", "West Bengal", "Bihar", "Assam", "Himachal Pradesh", 
              "Chandigarh", "Jammu and Kashmir", "Telangana", "Uttar Pradesh"] 
    
    selected_state = st.selectbox("Select a State", states)

    if selected_state is not None:
        df = pd.read_csv(states_to_files[selected_state])
        route_options = list(df[df.columns[0]])
        selected_route = st.selectbox("Select a Route", route_options)

    if selected_route is not None:
        col1, col2 = st.columns(2)
        with col1:
            selected_price = st.selectbox("Select Price Range", price_range)
            selected_time = st.selectbox("Select Departure Time", time_slots)
        with col2:
            selected_rating = st.selectbox("Select Rating", ratings)
            selected_seats = st.selectbox("Select Seat Availability", availability)

        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="project_one"
        )
        mycursor = mydb.cursor()

        # Price condition
        if selected_price == "100-500":
            price_condition = "price BETWEEN 100 AND 500"
        elif selected_price == "500-1000":
            price_condition = "price BETWEEN 500 AND 1000"
        else:
            price_condition = "price >= 1000"

        # Time condition
        time_conditions = {
            "Morning (06:00-12:00)": "departing_time BETWEEN '06:00' AND '12:00'",
            "Afternoon (12:00-18:00)": "departing_time BETWEEN '12:00' AND '18:00'",
            "Evening (18:00-24:00)": "departing_time BETWEEN '18:00' AND '24:00'",
            "Night (00:00-06:00)": "departing_time BETWEEN '00:00' AND '06:00'"
        }
        time_condition = time_conditions[selected_time]

        # Rating condition
        if selected_rating == "4★ & above":
            rating_condition = "star_rating >= 4"
        elif selected_rating == "3★ & above":
            rating_condition = "star_rating >= 3"
        else:
            rating_condition = "1=1"  # Always true   

        # Seat availability condition
        
        if selected_seats == "Very Limited (1-5 seats)":
            seat_condition = "seat_availability BETWEEN 1 AND 5"
        elif selected_seats == "Limited (6-10 seats)":
            seat_condition = "seat_availability BETWEEN 6 AND 10"
        elif selected_seats == "Available (11-20 seats)":
            seat_condition = "seat_availability BETWEEN 11 AND 20"
        elif selected_seats == "Many Available (20+ seats)":
            seat_condition = "seat_availability > 20"
        else:  # "All"
            seat_condition = "1=1"

        query = f"""
        SELECT * FROM bus_routes 
        WHERE route_name = %s 
        AND {price_condition}
        AND {time_condition}
        AND {rating_condition}
        AND {seat_condition}
        """
        
        mycursor.execute(query, (selected_route,))
        results = mycursor.fetchall()

        df = pd.DataFrame(results, columns=['ID', 'route_name', 'route_link', 'bus_name', 'bus_type', 
                                          'departing_time', 'duration', 'reaching_time', 'star_rating', 
                                          'price', 'seat_availability'])
        st.dataframe(df)
 
                           
