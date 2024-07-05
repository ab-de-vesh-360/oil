import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


st.title('2D Anisotropic Permability')
st.sidebar.title('Inputs')

kh= st.sidebar.slider('Horizontal Perm(md)',min_value = 100, max_value= 200, value= 200)
kt= st.sidebar.slider('Transverse Perm(md)',min_value = 0, max_value= 50, value= 50)

x = np.linspace(0,90,30)
y = np.radians(x)
k11 = kh*(np.cos(y))**2 + kt*(np.sin(y))**2
k22 = kh*(np.sin(y))**2 + kt*(np.cos(y))**2
k12_21 = (kh - kt)*(np.cos(y))*(np.sin(y))

b = st.button('Show Permeability Profile')

if b:  #tells if the button is pressed
    plt.style.use('classic')
    plt.figure(figsize=(6,8))
    fig,ax = plt.subplots()

    ax.plot(x,k11, label = 'k11')
    ax.plot(x,k22, label = 'k22')
    ax.plot(x,k12_21, label = 'k12_21')
    
    #ax.grid(True)
    #ax.set_xlabel('Angle(Degree)')
    #ax.set_ylabel('Permeabilities Tensor Elements(md)')
    #ax.legend()
    #ax.set_title('Permeability Profile')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=k11, mode='lines+markers', name='k11',
                         hovertemplate='Angle: %{x}<br>k11: %{y}'))
    fig.add_trace(go.Scatter(x=x, y=k22, mode='lines+markers', name='k22',
                         hovertemplate='Angle: %{x}<br>k22: %{y}'))
    fig.add_trace(go.Scatter(x=x, y=k12_21, mode='lines+markers', name='k12_21',
                         hovertemplate='Angle: %{x}<br>k12_21: %{y}'))
    hovermode='closest'
    
    fig.update_layout(
    title='2D Permeability Profile',
    xaxis_title='Angle (degrees)',
    yaxis_title='Permeabilities Tensor Elements(md)',
    hovermode='closest')
    st.plotly_chart(fig)
    
    #st.pyplot(fig)
      #for showing the fig in app    
