import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def plot_instance():
    st.set_page_config(layout="wide")
    user_input = st.sidebar.text_input("Database instance: ")
    return user_input

def plot_dashboard(databases, dbs, collections):
    
    df = pd.DataFrame.from_dict(dbs).transpose()
    #df_collections = pd.DataFrame.from_dict(collections)
    dbs_selected = ['----']
    for x in databases:
        dbs_selected.append(x)
    database = st.sidebar.selectbox("Database", dbs_selected)
    if(database == '----'):
        col1, col2 = st.columns(2)
        col3 = st.columns(1)
        
        fig_storage = px.pie(df, values="storageSize", names=df.index, title="Storage by Database")
        print(df)
        df_sorted = df.sort_values(by='collectionsNumber', ascending=False).head(5)
        print(df_sorted)
        fig_storage_sorted = px.bar(df_sorted, x='collectionsNumber', y=df_sorted.index, orientation='h', title="Collections by Database")
        fig_storage_sorted.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_storage_sorted.update_xaxes(range=[0, max(df_sorted['collectionsNumber'])])
        col1.plotly_chart(fig_storage, use_container_width=True)
        col2.plotly_chart(fig_storage_sorted, use_container_width=True)
        df_storage = df.sort_values(by='storageSize', ascending=False).head(5)
        fig_histogram = px.histogram(df_storage, barmode='group', x=df_storage.index, y=['storageSize','collectionsNumber', 'documents', 'indexes'])
        col3[0].plotly_chart(fig_histogram, use_container_width=True)
    else:
        plt.clf()
        st.empty()
    return database
    #df_collections

def plot_collections(database, collections):
    if(database == '----'):
        st.empty()
    else:
        col1, col2 = st.columns(2)
        col3 = st.columns(1)
        df = pd.DataFrame.from_dict(collections[database]).transpose()
        fig_storage = px.pie(df, values="storageSize", names=df.index, title="Storage by Collection")
        df_sorted = df.sort_values(by='documents', ascending=False).head(5)
        print(df_sorted)
        fig_storage_sorted = px.bar(df_sorted, x='documents', y=df_sorted.index, orientation='h', title="Collections by Database")
        fig_storage_sorted.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_storage_sorted.update_xaxes(range=[0, max(df_sorted['documents'])])
        col1.plotly_chart(fig_storage, use_container_width=True)
        col2.plotly_chart(fig_storage_sorted, use_container_width=True)
        df_storage = df.sort_values(by='storageSize', ascending=False).head(5)
        fig_histogram = px.histogram(df_storage, barmode='group', x=df_storage.index, y=['storageSize','indexesNumber', 'documents'])
        col3[0].plotly_chart(fig_histogram, use_container_width=True)