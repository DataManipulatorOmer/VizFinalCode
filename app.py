#Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
#******************************************************************************************************************************
# Loader
def loaderFunction(pathFile):
    data = pd.read_csv(pathFile)
    data = data.dropna(axis=1, how='all')
    return data
#******************************************************************************************************************************
def  caterNullVals(data, nullHandlingOption):
    if nullHandlingOption == "Remove Null":
        cleanedData = data.dropna()
        return cleanedData
    elif nullHandlingOption == "Impute by Mode":
        data_imputed = data.fillna(data.mode().iloc[0])
        return data_imputed
    else:
        return data
#****************************************************************************************************************************** 
# Configuration
st.set_page_config(page_title="Carbon Emission Data Analysis", layout="wide")
#******************************************************************************************************************************
# Welcome page
def welcomPage():
    st.title("Welcome to Carbon Emission Data Analysis")

    # introductory information 
    st.write(
        "This is your gateway to exploring and understanding Carbon Emission Data. "
        "Whether you're a researcher, student, or anyone interested in environmental data, "
        "you can use this app to gain insights into various aspects of carbon emissions around the world."
    )

    # brief overview 
    st.header("Key Analyses Available:")
    st.markdown(
        "- **Cement Carbon Emission:** Analyze carbon emissions specifically from the cement industry.\n"
        "- **Global Carbon Budget:** Explore the overall global carbon budget and its trends.\n"
        "- **Historical Budget:** Examine historical data on carbon emissions.\n"
        "- **Land Use Change Emission:** Understand the impact of land use changes on carbon emissions.\n"
        "- **Ocean Sink:** Investigate the role of oceans in absorbing carbon.\n"
        "- **Terrestrial Sink:** Explore how terrestrial ecosystems contribute to carbon absorption.\n"
        "- **Consumption Emission:** Analyze carbon emissions based on consumption patterns.\n"
        "- **Emission Transfer:** Understand the transfer of emissions between regions.\n"
        "- **Territorial Emission:** Explore carbon emissions specific to territories."
    )

    # call-to-action
    st.markdown(
        "Ready to dive in? Use the navigation bar on the left to explore different analyses. "
        "Click on 'Get Started' when you're ready to begin your journey into Carbon Emission Data Analysis."
    )

    #  get started
    if st.button("Get Started"):
        st.success("Great! Let's get started with the analysis.")
#******************************************************************************************************************************
# Cement Carbon Emission
def cementEmissionPage():
    st.title("Cement Carbon Emission Analysis")
    
    # Upload CSV file
    pathFile = st.file_uploader("Upload CSV file for Cement Carbon Emission", type=["csv"])
    
    if pathFile is not None:
        data = loaderFunction(pathFile)
        
        # Display uploaded data
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        
        # Handle null values
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        if nullHandlingOption != "Keep Null":
            data = caterNullVals(data, nullHandlingOption)
            st.success(f"Null values Handled Successfully: {nullHandlingOption}")
        
        # Plot 1: Line Plot for GCB over the Years
        fig1 = px.line(data, x='Year', y='GCB', title='Cement Carbon Emission (Global Carbon Emission) over the Years')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**Storytelling Question 1:** How has GCB emissions changed over the years?")
        
        # Plot 2: Scatter Plot for Cao and Huang
        fig2 = px.scatter(data, x='Cao', y='Huang', title='Scatter Plot: Cao (Calcium-based sorbents) vs Huang')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Storytelling Question 2:** Is there a correlation between Cao and Huang emissions?")
        
        # Plot 3: Bar Chart for Total Emissions in a Specific Year
        yearSelect = st.slider("Select a Year:", min_value=int(data['Year'].min()), max_value=int(data['Year'].max()))
        dataSelect = data[data['Year'] == yearSelect]
        fig3 = px.bar(dataSelect, x='Year', y=['GCB', 'Cao', 'Huang'], barmode='group',
                     title=f'Emission Breakdown for the Year {yearSelect}')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Storytelling Question 3:** How does the emission composition change in a specific year?")
        
        # Plot 4: Box Plot for GCB Emissions
        fig4 = px.box(data, y='GCB', title='Box Plot: Distribution of GCB Emissions')
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("**Storytelling Question 4:** What is the distribution of GCB emissions?")
        
        # Plot 5: Area Chart for Cumulative Cao Emissions over the Years
        data['Cumulative_Cao'] = data['Cao'].cumsum()
        fig5 = px.area(data, x='Year', y='Cumulative_Cao', title='Cumulative Cao Emissions over the Years')
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("**Storytelling Question 5:** How does Cao emissions accumulate over the years?")
        
#******************************************************************************************************************************    
# Global Carbon Budget
def globalCarbonBudgetPage():
    st.title("Global Carbon Budget Analysis")
    
    # Upload CSV file
    pathFile = st.file_uploader("Upload CSV file for Global Carbon Budget", type=["csv"])
    
    if pathFile is not None:
        data = loaderFunction(pathFile)
        
        # Display uploaded data
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        
        # Handle null values
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        if nullHandlingOption != "Keep Null":
            data = caterNullVals(data, nullHandlingOption)
            st.success(f"Null values Handled Successfully: {nullHandlingOption}")
        st.write("Budget imbalance refers to a situation where there is a disparity between a government's revenue and its expenditures within a specified period, typically a fiscal year. ")   
#******************************************************************************************************************************
        rangeForYear = st.slider("Select Year Range:", min_value=int(data['Year'].min()), 
                               max_value=int(data['Year'].max()), value=(int(data['Year'].min()), int(data['Year'].max())))
        
#******************************************************************************************************************************
        fig1 = px.line(data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])], 
                       x='Year', y='fossil emissions excluding carbonation',
                       title='Fossil Emissions (excluding carbonation) over the Years',
                       labels={'fossil emissions excluding carbonation': 'Fossil Emissions'})
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**Storytelling Question 1:** How have fossil emissions (excluding carbonation) changed over the selected years?")
        
#******************************************************************************************************************************
        fig2 = px.area(data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])], 
                       x='Year', y=['ocean sink', 'land sink', 'cement carbonation sink'],
                       title='Distribution of Carbon Sinks over the Years', 
                       labels={'value': 'Carbon Sink'})
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Storytelling Question 2:** What is the contribution of different sinks to the carbon budget over the selected years?")
        
 #******************************************************************************************************************************
        fig3 = px.bar(data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])], 
                      x='Year', y='budget imbalance', color='budget imbalance',
                      title='Budget Imbalance over the Years', 
                      labels={'budget imbalance': 'Budget Imbalance'})
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Storytelling Question 3:** How does the budget imbalance vary from year to year in the selected range?")
#******************************************************************************************************************************
#  Historical Budget
def historicalBudgetPage():
    st.title("Historical Budget Analysis")
    
    # Upload CSV file
    pathFile = st.file_uploader("Upload CSV file for Historical Budget", type=["csv"])
    
    if pathFile is not None:
        data = loaderFunction(pathFile)
        
        # Display uploaded data
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        
        # Handle null values
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        if nullHandlingOption != "Keep Null":
            data = caterNullVals(data, nullHandlingOption)
            st.success(f"Null values Handled Successfully: {nullHandlingOption}")
        
#******************************************************************************************************************************
        rangeForYear = st.slider("Select Year Range:", min_value=int(data['Year'].min()), 
                               max_value=int(data['Year'].max()), value=(int(data['Year'].min()), int(data['Year'].max())))
        
#******************************************************************************************************************************
        fig1 = px.line(data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])], 
                       x='Year', y='fossil emissions excluding carbonation',
                       title='Fossil Emissions (excluding carbonation) over the Years',
                       labels={'fossil emissions excluding carbonation': 'Fossil Emissions'})
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**Storytelling Question 1:** How have fossil emissions (excluding carbonation) changed over the selected years?")
#******************************************************************************************************************************
        fig2 = px.area(data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])], 
                       x='Year', y=['atmospheric growth', 'ocean sink', 'land sink'],
                       title='Components of Carbon Budget over the Years', 
                       labels={'value': 'Carbon Budget Component'})
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Storytelling Question 2:** What are the contributions of different components to the carbon budget over the selected years?")
#******************************************************************************************************************************
        fig3 = px.bar(data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])], 
                      x='Year', y='budget imbalance', color='budget imbalance',
                      title='Budget Imbalance over the Years', 
                      labels={'budget imbalance': 'Budget Imbalance'})
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Storytelling Question 3:** How does the budget imbalance vary from year to year in the selected range?")
#******************************************************************************************************************************
#  Land Use Change Emission
def landUseChangeEmissionPage():
    st.title("Land Use Change Emission Analysis")
    
    # Upload CSV file
    pathFile = st.file_uploader("Upload CSV file for Land Use Change Emission", type=["csv"])
    
    if pathFile is not None:
        data = loaderFunction(pathFile)
        
        # Display uploaded data
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        
        # Handle null values
        handleNullValueOptions = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        if handleNullValueOptions != "Keep Null":
            data = caterNullVals(data, handleNullValueOptions)
            st.success(f"Null values handled successfully: {handleNullValueOptions}")    
#******************************************************************************************************************************
        rangeForYear = st.slider("Select Year Range:", min_value=int(data['Year'].min()), 
                               max_value=int(data['Year'].max()), value=(int(data['Year'].min()), int(data['Year'].max())))
        
#******************************************************************************************************************************
        transSelect = st.multiselect("Select Land Use Change Transitions:", list(data.columns[2:7]), default=list(data.columns[2:7]))
#******************************************************************************************************************************
        dataFiltereddd = data[(data['Year'] >= rangeForYear[0]) & (data['Year'] <= rangeForYear[1])]
        if transSelect:
            dataFiltereddd = dataFiltereddd[transSelect + ['Year']]
#******************************************************************************************************************************
        fig1 = px.line(dataFiltereddd, x='Year', y=transSelect,
                       color_discrete_sequence=px.colors.qualitative.Set1,
                       title='Net Deforestation over the Years', 
                       labels={'value': 'Net Deforestation'})
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**Storytelling Question 1:** How does net deforestation vary over the selected years and transitions?")
#******************************************************************************************************************************
        fig2 = px.bar(dataFiltereddd, x='Year', y='forest regrowth (total)',
                      color='forest regrowth (total)',
                      title='Total Forest Regrowth over the Years', 
                      labels={'forest regrowth (total)': 'Total Forest Regrowth'})
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Storytelling Question 2:** What is the pattern of total forest regrowth over the selected years?")
#******************************************************************************************************************************
        fig3 = px.scatter(dataFiltereddd, x='deforestation (total)', y='forest regrowth (total)',
                          color='Year', size='wood harvest & other forest management',
                          title='Net Deforestation vs. Forest Regrowth', 
                          labels={'Net deforestation (total)': 'Net Deforestation', 'forest regrowth (total)': 'Forest Regrowth'})
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Storytelling Question 3:** How is the relationship between net deforestation and forest regrowth?")
#******************************************************************************************************************************
        fig4 = px.area(dataFiltereddd, x='Year', y=transSelect,
                       title='Area Chart for Land Use Change Transitions Over the Years', 
                       labels={'value': 'Land Use Change'})
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("**Storytelling Question 4:** How do different land use change transitions evolve over the years?")
#******************************************************************************************************************************        
        # fig5 = px.area(dataFiltereddd, x='Year', y=transSelect,
        #                title='Stacked Area Chart for Land Use Change Transitions Over the Years', 
        #                labels={'value': 'Land Use Change'}, 
        #                color_discrete_sequence=px.colors.qualitative.Set2)
        # st.plotly_chart(fig5, use_container_width=True)
        # st.markdown("**Question 5:** Explore the stacked area chart to observe the contributions of different land use change transitions over the years.")
        
#******************************************************************************************************************************
#  Ocean Sink
def oceanSinkPage():
    st.title("Ocean Sink Analysis")
    #  Ocean Sink
    pathFile = st.file_uploader("Upload CSV file for Ocean Sink", type=["csv"])
    if pathFile is not None:
        data = loaderFunction(pathFile)
        st.success("File successfully uploaded and loaded!")
        st.write("The ocean acts as a “carbon sink” and absorbs about 31% of the CO2 emissions released into the atmosphere according to a study published by NOAA and international partners in Science.")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
            data =  caterNullVals(data, nullHandlingOption)
        st.success(f"Null values Handled Successfuly : {nullHandlingOption}")
        st.write("Data After Removing Nulls") 
        st.write(data.isnull().sum())         
#******************************************************************************************************************************
#  Terrestrial Sink
def terrestrialSinkPage():
    st.title("Terrestrial Sink Analysis")

    # Terrestrial Sink
    pathFile = st.file_uploader("Upload CSV file for Terrestrial Sink", type=["csv"])
    
    if pathFile is not None:
        data = pd.read_csv(pathFile)
        st.success("File successfully uploaded and loaded!")
        st.write("A terrestrial sink, in this context, refers to the capacity of terrestrial ecosystems such as forests, grasslands, and soils to absorb and store carbon dioxide (CO2) from the atmosphere through processes like photosynthesis and biomass accumulation. ")
        st.subheader("Data Summary:")
        st.write(data.head())  
        
        st.subheader("Data Types:")
        st.write(data.dtypes)  
        
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  

        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
            data = caterNullVals(data, nullHandlingOption)
        st.success(f"Null values Handled Successfully: {nullHandlingOption}")
#******************************************************************************************************************************
#  Consumption Emission
def consumptionEmissionPage():
    st.title("Consumption Emission Analysis")
    #  Consumption Emission
    pathFile = st.file_uploader("Upload CSV file for Consumption Emission", type=["csv"])
    if pathFile is not None:
        data = loaderFunction(pathFile)
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
            data =  caterNullVals(data, nullHandlingOption)
        st.success(f"Null values Handled Successfuly : {nullHandlingOption}") 
        st.subheader("Consumption Emission Country-wise:")
        
#******************************************************************************************************************************
        countryColumns = data.columns[1:]
#******************************************************************************************************************************
        meltedCols = pd.melt(data, id_vars=['Year'], value_vars=countryColumns, var_name='Country', value_name='Consumption Emission')
#******************************************************************************************************************************
        yearSelect = st.slider("Select Year", min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), value=int(data['Year'].max()))
#******************************************************************************************************************************
        yearlySelectedData = meltedCols[meltedCols['Year'] == yearSelect]
#******************************************************************************************************************************
        figCount = go.Figure()

        figCount.add_trace(go.Bar(x=yearlySelectedData['Country'], y=yearlySelectedData['Consumption Emission'], name=str(yearSelect)))

        figCount.update_layout(xaxis_title='Country', yaxis_title='Consumption Emission', title=f'Consumption Emission Country-wise for {yearSelect}')
        
        st.plotly_chart(figCount)
#******************************************************************************************************************************
#  Emission Transfer
def emissionTransferPage():
    st.title("Emission Transfer Analysis")
    #  Emission Transfer
    pathFile = st.file_uploader("Upload CSV file for Emission Transfer", type=["csv"])
    if pathFile is not None:
        data = loaderFunction(pathFile)
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
            data =  caterNullVals(data, nullHandlingOption)
        st.success(f"Null values Handled Successfuly : {nullHandlingOption}")
#******************************************************************************************************************************
        countryColumns = data.columns[1:]
        meltedCols = pd.melt(data, id_vars=['Year'], value_vars=countryColumns, var_name='Country', value_name='Emission Transfer')
 #******************************************************************************************************************************
        yearSelect = st.slider("Select Year", min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), value=int(data['Year'].max()))
#******************************************************************************************************************************
        yearlySelectedData = meltedCols[meltedCols['Year'] == yearSelect]
#******************************************************************************************************************************
        figCount = go.Figure()

        figCount.add_trace(go.Bar(x=yearlySelectedData['Country'], y=yearlySelectedData['Emission Transfer'], name=str(yearSelect)))

        figCount.update_layout(xaxis_title='Country', yaxis_title='Emission Transfer', title=f'Emission Transfer Country-wise for {yearSelect}')
        
        st.plotly_chart(figCount)
#******************************************************************************************************************************
#  Territorial Emission
def territorialEmissionPage():
    st.title("Territorial Emission Analysis")
    #  Territorial Emission
    pathFile = st.file_uploader("Upload CSV file for Territorial Emission", type=["csv"])
    if pathFile is not None:
        data = loaderFunction(pathFile)
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
            data =  caterNullVals(data, nullHandlingOption)
        st.success(f"Null values Handled Successfuly : {nullHandlingOption}")
#******************************************************************************************************************************
        countryColumns = data.columns[1:]
#******************************************************************************************************************************
        meltedCols = pd.melt(data, id_vars=['Year'], value_vars=countryColumns, var_name='Country', value_name='Emission Transfer')
#******************************************************************************************************************************
        yearSelect = st.slider("Select Year", min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), value=int(data['Year'].max()))
#******************************************************************************************************************************
        yearlySelectedData = meltedCols[meltedCols['Year'] == yearSelect]
#******************************************************************************************************************************
        figCount = go.Figure()
#******************************************************************************************************************************
        figCount.add_trace(go.Bar(x=yearlySelectedData['Country'], y=yearlySelectedData['Emission Transfer'], name=str(yearSelect)))
#******************************************************************************************************************************
        figCount.update_layout(xaxis_title='Country', yaxis_title='Emission Transfer', title=f'Emission Transfer Country-wise for {yearSelect}')
        
        st.plotly_chart(figCount)
#******************************************************************************************************************************
def fossilEmissionPage():
    st.title("Fossil Emission Analysis")
    #  Territorial Emission
    pathFile = st.file_uploader("Upload CSV file for Fossil Emission", type=["csv"])
    if pathFile is not None:
        data = loaderFunction(pathFile)
        st.success("File successfully uploaded and loaded!")
        st.subheader("Data Summary:")
        st.write(data.head())  
        st.subheader("Data Types:")
        st.write(data.dtypes) 
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())  
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
            data =  caterNullVals(data, nullHandlingOption)
        st.success(f"Null values Handled Successfuly : {nullHandlingOption}")
#******************************************************************************************************************************
def fossilEmissionPage():
    st.title("Fossil Emission Analysis")
    
    # Territorial Emission
    pathFile = st.file_uploader("Upload CSV file for Fossil Emission", type=["csv"])
    
    if pathFile is not None:
        data = pd.read_csv(pathFile)
        st.success("File successfully uploaded and loaded!")
        
        st.subheader("Data Summary:")
        st.write(data.head())
        
        st.subheader("Data Types:")
        st.write(data.dtypes)
        
        st.subheader("Total Null Values:")
        st.write(data.isnull().sum())
        
        nullHandlingOption = st.selectbox("How to handle null values:", ["Remove Null", "Impute by Mode", "Keep Null"])
        
        if nullHandlingOption != "Keep Null":
#******************************************************************************************************************************
            data = caterNullVals(data, nullHandlingOption)
        
        st.success(f"Null values handled successfully: {nullHandlingOption}")
#******************************************************************************************************************************
        st.subheader("Fossil Emissions Over the Years:")
#******************************************************************************************************************************
        figFossilEmission = px.line(data, x='Year', y=['fossil.emissions.excluding.carbonation', 'Coal', 'Oil', 'Gas', 'Cement.emission', 'Flaring', 'Other'],
                                       title='Fossil Emissions Over the Years',
                                       labels={'value': 'Emissions', 'Year': 'Year'},
                                       line_shape='linear',
                                       template='plotly_dark')

        st.plotly_chart(figFossilEmission)
#******************************************************************************************************************************
# Navigation bar
selected_page = st.sidebar.selectbox("Select Page", ["Welcome", "Cement Carbon Emission", "Global Carbon Budget",
                                                     "Historical Budget", "Land Use Change Emission", "Ocean Sink",
                                                     "Terrestrial Sink", "Consumption Emission", "Emission Transfer",
                                                     "Territorial Emission","Fossil Emission"])

# Load data 
if selected_page == "Welcome":
    welcomPage()
elif selected_page == "Cement Carbon Emission":
    cementEmissionPage()
elif selected_page == "Global Carbon Budget":
    globalCarbonBudgetPage()
elif selected_page == "Historical Budget":
    historicalBudgetPage()
elif selected_page == "Land Use Change Emission":
    landUseChangeEmissionPage()
elif selected_page == "Ocean Sink":
    oceanSinkPage()
elif selected_page == "Terrestrial Sink":
    terrestrialSinkPage()
elif selected_page == "Consumption Emission":
    consumptionEmissionPage()
elif selected_page == "Emission Transfer":
    emissionTransferPage()
elif selected_page == "Territorial Emission":
    territorialEmissionPage()
elif selected_page == "Fossil Emission":
    fossilEmissionPage()
    



































