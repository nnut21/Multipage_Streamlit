import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from urllib.error import URLError
import time
st.set_page_config(
    page_title="Starbucks Demo",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#st.set_page_config(page_title="Starbucks Demo", page_icon="🥤")

st.markdown("# :green[Starbucks] :mermaid: Demo")

st.sidebar.header("Starbucks Demo")

#st.write("## Raw Data")

# cache the CSV loading process
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nnut21/DADS5001_Data_Analysis/refs/heads/main/dataset/Starbucks.csv?token=GHSAT0AAAAAAC2H4XDZLHHBXMDDZR324Q3IZZR4R4A"
    df = pd.read_csv(url)
    return df
def get_country_data():
    df = pd.read_csv("https://raw.githubusercontent.com/imyajaii/dads5001-mini-project-01/refs/heads/main/dataset/countryContinent.csv",encoding='latin-1')
    return df#.set_index('country')

# Load the data
df_stb = load_data()
df = get_country_data()

#Transform country
df_country = df[['code_2','country']]
df_country = df_country.set_index('code_2')

#df_country
new_df = df_country.merge(df_stb, left_on='code_2', right_on='Country')
new_df = new_df.drop(['Country'],axis = 1)
new_df = new_df.set_index('country')



if st.checkbox('Show data of starbucks'):
    st.subheader('Data After clean')
    st.write(new_df.head(5))


st.divider()

st.subheader("Top 10 of the country that have the Most :green[starbucks] cafe in the world")
col = st.columns((1, 1.5), gap='medium')
with col[0]:
#st.write(data2)
    data = new_df.value_counts('country').sort_values(ascending=False)
#st.write(data)
#data.columns()

#st.dataframe(data)
    top_data = data.head(10).to_frame()

    st.dataframe(
        top_data,
        column_order=("country", "count"),
        column_config={
            "country": st.column_config.TextColumn("Country"),
            "count": st.column_config.ProgressColumn(
                "Count",
                format="%d",
                min_value=0,
                max_value=int(top_data["count"].max())
            ),
        },
    )
with col[1]:
    #st.write('## Use streamlit #')
    #st.bar_chart(data,x_label='country',y_label='Amount of Store')

    #st.write('## Use plotly #')
    #color = st.color_picker("Color", "#FF0000")
    sequential_palettes = [
    "Viridis", "Plasma", "Cividis", "Inferno", "Magma",
    "Greens", "Blues", "Reds", "Oranges", "Purples", "Greys"]

    fig = px.bar(top_data, y='count', color='count', color_continuous_scale='Cividis',height = 500)
    fig

st.divider()

st.subheader('Map of all stores')
map = new_df.drop(new_df.loc[new_df['Longitude'].isna()].index, inplace=True)
st.map(new_df,latitude='Latitude', longitude='Longitude', size =100 )

###P'Palm

new_df['Store Info'] = new_df['Store Name'] + " (" + new_df['Ownership Type'] + ")"

# Sidebar for country selection
new_df= new_df.reset_index()

countries = new_df['country'].unique()
selected_country = st.sidebar.selectbox("Select a Country", ['All'] + list(countries))

# Filter data based on selected country
if selected_country != 'All':
   new_df = new_df[new_df['country'] == selected_country]
   city = new_df['City'].unique()
   #For Check
   #st.write(int(len(city)))

else:city = new_df['City'].unique()

# Plotly scatter mapbox for geographical mapping
fig = px.scatter_mapbox(new_df,
                        lat="Latitude",
                        lon="Longitude",
                        hover_name="Store Info",
                        hover_data={"City": True, "State/Province": True},
                        color="Ownership Type",
                        zoom=3,
                        title=f"Store Locations in {selected_country if selected_country != 'All' else 'All Countries'}")

# Set the map style
fig.update_layout(mapbox_style="carto-positron", height=600)

# Display the map
st.plotly_chart(fig)

# Optional: Display filtered data table

#st.subheader("Filtered Data")
if st.checkbox('Show data of starbucks store information'):
    #st.subheader('Data After clean')
    #st.write(new_df.head(5))
    if selected_country != 'All':
        total_store = int(new_df.value_counts('country'))
        st.write(f'#### Total Starbucks of',selected_country,'is',total_store,'stores')
    # Filter data based on selected city
        selected_city = st.selectbox("Select a City", ['All'] + list(city))
        if selected_city != 'All':
            new_df = new_df[new_df['City'] == selected_city] 
    else: st.write(f'#### 🌍 Total of :green[Starbucks] stores around the world is',)
        
    st.dataframe(new_df[['country','Store Name', 'City', 'State/Province', 'Ownership Type']])

st.divider()


st.subheader('Use plotly Select country for Bar Chart')
#new_df = new_df.set_index('country')
try:
    countries = st.multiselect(
        "Choose countries", list(new_df['country'].unique()), ["Thailand", "Viet Nam", "Malaysia", "Singapore"]
        )
    if not countries:
            st.error("Please select at least one country.")
    else:
        data_chart = data.loc[countries]
        col = st.columns((1, 4), gap='medium')
        with col[0]:
            st.write("### Selected countries", data_chart.sort_index())
        with col[1]:
            fig = px.bar(data_chart, y='count', color='count', color_continuous_scale='Cividis')
            fig
        
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )