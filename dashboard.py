import streamlit as st
import pandas as pd
import plotly.express as px

def plot_dashboard(databases, dbs, collections):
    st.set_page_config(layout="wide")
    
    df = pd.DataFrame.from_dict(dbs).transpose()
    #df_collections = pd.DataFrame.from_dict(collections)
    database = st.sidebar.selectbox("Database", databases)
    col1, col2 = st.columns(2)
    
    fig_storage = px.pie(df, values="storageSize", title="Storage by Database")
    df_sorted = df.sort_values(by='storageSize', ascending=False).head(5)
    print(df_sorted)
    fig_storage_sorted = px.bar(df_sorted, x=df_sorted['storageSize'], y=df_sorted.index, orientation='h', x)
    fig_storage_sorted.update_layout(yaxis={'categoryorder':'total ascending'})
    col1.plotly_chart(fig_storage, use_container_width=True)
    col2.plotly_chart(fig_storage_sorted, use_container_width=True)
    #df_collections
    