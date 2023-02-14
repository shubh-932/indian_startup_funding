import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='StartUp Analysis')

df = pd.read_excel("startup_funding.xlsx")

##-------------------------------------------------------data cleaning steps------------------------------------------------
df.set_index("Sr No", inplace=True)

df["amount"].fillna(0, inplace=True)

df["date"] = pd.to_datetime(df["date"], errors='coerce')

df.dropna(subset=['date', 'startup', 'vertical', 'city', 'investors', 'round', 'amount'], inplace=True)

df['month'] = df.date.dt.month
df['year'] = df.date.dt.year

##-------------------------------------------------------xxxxxxxxxxxxxxxxxxx------------------------------------------------



def investor_pov(investor):

    st.subheader(investor)

    recent_investments = df[df['investors'].str.contains(investor)].sort_values('date', ascending=False).head(5)[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.write("Recent Investments")
    st.dataframe(recent_investments)

    col1, col2 = st.columns(2)

    with col1:
        biggest_investments = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5).reset_index()
        st.write("Biggest Investments")
        st.bar_chart(biggest_investments, x='startup', y='amount')
    
    with col2:
        yoy = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum().reset_index()
        st.write("YoY Investments")
        st.line_chart(yoy, x='year', y='amount')


    st.write("Generally invests in....")
    col1, col2, col3 = st.columns(3)

    with col1:
        vertical = df[df['investors'].str.contains(investor)]['vertical'].value_counts()
        st.write("SECTOR")
        fig, ax = plt.subplots()
        ax.pie(vertical.values, labels=vertical.index, autopct="%0.1f%%")
        st.pyplot(fig)
    with col2:
        round = df[df['investors'].str.contains(investor)]['round'].value_counts()
        st.write("STAGE")
        fig, ax = plt.subplots()
        ax.pie(round.values, labels=round.index, autopct="%0.1f%%")
        st.pyplot(fig)
    with col3:
        city = df[df['investors'].str.contains(investor)]['city'].value_counts()
        st.write("CITY")
        fig, ax = plt.subplots()
        ax.pie(city.values, labels=city.index, autopct="%0.1f%%")
        st.pyplot(fig)


##----------------------------------------------------------app building----------------------------------------------------
st.sidebar.title("Indian Startup Funding Analysis")
option = st.sidebar.selectbox("Select", ['Overall Analysis', 'StartUp', 'Investor'])

if option == "Overall Analysis":
    st.title("Overall Analysis")
    

elif option == "StartUp":
    st.title("StartUp Analysis")
    st.sidebar.selectbox("Select StartUp", sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find StartUp Details")

else:
    st.title("Investor Analysis")
    investor = st.sidebar.selectbox("Select Investor", sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")

    if btn2:
        investor_pov(investor)