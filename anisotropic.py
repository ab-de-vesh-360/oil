import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    plt.figure(figsize=(8,6))
    fig,ax = plt.subplots()

    ax.plot(x,k11, label = 'k11')
    ax.plot(x,k22, label = 'k22')
    ax.plot(x,k12_21, label = 'k12_21')
    
    ax.grid(True)
    ax.set_xlabel('Angle(Degree)')
    ax.set_ylabel('Permeabilities Tensor Elements(md)')
    ax.legend()
    ax.set_title('Permeability Profile')
    

    st.pyplot(fig)  #for showing the fig in app    
