## 💱 Live Currency Converter (Streamlit + API + SQLite)

A real-time currency conversion web app built with Python, Streamlit, and Frankfurter Exchange Rate API.
It converts between 30+ global currencies, stores history in a local database, and visualizes historical trends using interactive charts.

## 🔹 Features

🌍 Real-Time Conversion: Fetches live exchange rates using the Frankfurter REST API.

🧾 Smart History Tracking: Saves the last 10 conversions in a local SQLite database.

📊 Interactive Charts: Plotly graphs display exchange rate trends for any date range (1999–present).

🔄 Dynamic Currency List: Dropdown auto-loads all supported currencies with full names.

🧠 Clean UI: Streamlit front-end with responsive layout and intuitive controls.

🗃️ Offline Storage: Uses SQLite for persistent local storage of recent conversions.

## 🔹 Tech Stack

Frontend: Streamlit

Backend: Python

Database: SQLite3

API: Frankfurter Exchange Rate API

Visualization: Plotly

## 🔹 Future Enhancements

Export conversion history as CSV

Integrate user authentication

Add currency converter for crypto assets

<img width="1902" height="972" alt="image" src="https://github.com/user-attachments/assets/60bff77e-6818-4c83-af26-988a6903d90d" />
<img width="906" height="771" alt="image" src="https://github.com/user-attachments/assets/7736fa0b-3757-4361-b466-39eb0c51e6bc" />


## For app.py file (this has a frontend file)
STEPS
1.Install dependencies

pip install streamlit plotly requests


2.Run the app

streamlit run app.py

3.Key stepup
API_KEY = "key from the website "
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency.upper()}"

https://www.exchangerate-api.com/ 
Go this website get the keys and paste the in this "key from the website " path 

## For Currency_converter.py file 
STEPS
1.Install dependencies

pip install requests


2.Run the app

python currency_converter.py

3.3.Key stepup
API_KEY = "key from the website "
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency.upper()}"

https://www.exchangerate-api.com/ 
Go this website get the keys and paste the in this "key from the website " path  
Output:<img width="1200" height="146" alt="image" src="https://github.com/user-attachments/assets/8128d135-41f9-430c-82de-5d510f02da44" />

(there will be two files currency_converter.py and app.py , use app.py for the streamlit frontened ,basic use currency_converter.py)
