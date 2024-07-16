import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import plotly.graph_objects as go

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page != 'home':
    if st.sidebar.button('Home'):
        st.session_state.page = 'home'
if st.session_state.page == 'home':
    # Initial interface with title and description
    st.markdown("<h1 style='text-align: center; font-size: 50px;text-decoration: underline; margin-bottom: 0; color: dark brown;'>Directional Drilling Profiles</h1>", unsafe_allow_html=True)
    st.markdown("*<h2 style='text-align: right; font-size: 20px;text-decoration: italy; margin-bottom: 0; color: green;'>Unleash the Trajectory!!</h2>*", unsafe_allow_html=True)
    st.markdown("*Welcome to the Directional Drilling Profile Trajectory Calculator!*  \n    \n  *This tool is designed to assist drilling engineers and geologists in calculating and visualizing the trajectory of directional drilling profiles. By inputting key parameters such as Kick off Point, vertical depth of Target, horizontal distance to Target, and other corner values, this calculator provides accurate and efficient calculations of drilling trajectories. Whether you're planning a new well or analyzing an existing profile, our calculator helps you determine the build and hold sections of your drilling path, ensuring precision in achieving desired targets. With interactive visualizations and user-friendly interfaces, you can easily monitor the different parameters at any point along the path to the target.*")
    
    input_method = st.radio('**Please Select the Type of Drilling profile:**', ('Build and Hold Profile', 'Build, Hold and Drop Profile'), index = None)

    if input_method == 'Build and Hold Profile':
        st.session_state.page = 'Build_Hold'
        st.rerun()
    elif input_method == 'Build, Hold and Drop Profile':
        st.session_state.page = 'Build_Hold_Drop'
        st.rerun()

elif st.session_state.page == 'Build_Hold':
    st.sidebar.title('Enter the known Parameters required')
    Vb = st.sidebar.number_input('Enter KOP Depth (ft)', value=1000.0, min_value=0.0, step = 0.01)
    Vt = st.sidebar.number_input('Enter TVD of Target (ft)', value=10000.0, min_value=0.0, step = 0.01)
    Ht = st.sidebar.number_input('Enter Horizontal Distance to Target (ft)', value=6000.0, min_value=0.0, step = 0.01)
    build_rate = st.sidebar.number_input('Enter Build Rate (degrees per 100 ft)', value=1.5, min_value=0.0, step = 0.01)
    
    def radius_of_curvature(build_rate):
       return 18000 / (np.pi * build_rate)
    r = radius_of_curvature(build_rate)

    def Inclination_angle(Ht, Vt, Vb, r ):
       X = np.arctan((Ht - r)/(Vt - Vb))
       Y = np.arcsin((r*np.cos(X))/(Vt - Vb))
       return np.degrees(X) + np.degrees(Y)
    a = Inclination_angle(Ht, Vt, Vb, r)

    Vc = Vb + r*np.sin(np.radians(a))
    Hc = r*(1-np.cos(np.radians(a)))
    MDc = Vb + (a/build_rate)*100
    MDt = MDc + (Vt - Vc)/np.cos(np.radians(a))
    b = st.sidebar.button('Show the Profile Trajectories')
    if b:

        st.sidebar.write(f'Calculated Radius: {r:.2f} ft')
        st.sidebar.write(f'Calculated Inclination Angle: {a:.2f}°')

        trajectory = {
           'Point': ['Start', 'Kick Off', 'End of Build-Up', 'Target'],
           'V(FT)': [0, Vb, Vc, Vt],
           'H(FT)': [0, 0, Hc, Ht],
           'MD(FT)': [0, Vb, MDc, MDt]
           }
        
        df = pd.DataFrame(trajectory)
        #st.dataframe(df, width=1000, height=200)
        st.header('***The Profile trajectory is shown as below:***')
        st.table(df)

        MDx_values = np.linspace(0, MDt, 10000)
        Vx_values = []
        Hx_values = []
        a_values = []

        for MDx in MDx_values:
            if MDx <= Vb:
                Vx = MDx
                Hx = 0
                a_x = 0
            elif MDx <= MDc:
                a1 = (MDx - Vb)*build_rate/100
                Vx = Vb + r*np.sin(np.radians(a1))
                Hx = r*(1-np.cos(np.radians(a1)))
                a_x = a1
            else:
                CX = MDx - MDc
                Vx = Vc + CX*np.cos(np.radians(a))
                Hx = Hc + CX*np.sin(np.radians(a))
                a_x = a
            Vx_values.append(Vx)
            Hx_values.append(Hx)
            a_values.append(a_x)
        
        fig, ax = plt.subplots()
        ax.plot(Hx_values,Vx_values , label='Build and Hold Trajectory')
        
        # ax.set_xlabel('Horizontal Distance (ft)')
        # ax.set_ylabel('Vertical Depth (ft)')
        # ax.set_title('Build and Hold Profile')
        # ax.legend()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Hx_values, y=Vx_values, mode='lines', name='Build and Hold Trajectory',
                         hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Inclination: %{customdata[1]}°', customdata=np.column_stack((MDx_values, a_values)), line=dict(width= 4)))
        

        # st.pyplot(fig)
        fig.update_layout(
        title='Build and Hold Profile',
        xaxis_title='Horizontal Distance (ft)',
        yaxis_title='Vertical Depth (ft)',
        yaxis=dict(
        autorange='reversed'),
        hovermode='closest')
        st.plotly_chart(fig)

        # Display the data
        st.subheader('Buil and Hold Trajectory Data')
        st.write(pd.DataFrame({'Measured Depth (MD),ft': MDx_values, 'Vertical Depth (v), ft': Vx_values, 'Horizontal Distance (H), ft': Hx_values, 'Inclination Angle (°)' : a_values}))

elif st.session_state.page == 'Build_Hold_Drop':
    st.sidebar.title('Enter the known Parameters required')
    Vb = st.sidebar.number_input('Enter KOP Depth (ft)', value=1000.0, min_value=0.0, step = 0.01)
    Vt = st.sidebar.number_input('Enter TVD of Target (ft)', value=10000.0, min_value=0.0, step = 0.01)
    Ht = st.sidebar.number_input('Enter Horizontal Distance to Target (ft)', value=6000.0, min_value=0.0, step = 0.01)
    Ve = st.sidebar.number_input('Enter the Vertical Distance to the End of Drop (ft)', value=8000.0, min_value=0.0, step=0.01)
    build_rate_1 = st.sidebar.number_input('Enter Build Rate 1 (degrees per 100 ft)', value=1.5, min_value=0.0, step = 0.01)
    build_rate_2 = st.sidebar.number_input('Enter Build Rate 1 (degrees per 100 ft)', value=2.0, min_value=0.0, step = 0.01)
    a2 = st.sidebar.number_input('Enter the Inclination angle after Drop (degrees)', value=20.0, min_value=0.0, step=0.01)

    def radius_of_curvature(build_rate):
        return 18000 / (np.pi * build_rate)
    r1 = radius_of_curvature(build_rate_1)
    r2 = radius_of_curvature(build_rate_2)
    OQ = Ht - r1 - r2*np.cos(np.radians(a2)) - (Vt - Ve)*np.tan(np.radians(a2))
    OP = Ve - Vb + r2*np.sin(np.radians(a2))
    QS = r1+r2
    PQ = np.sqrt(OP**2 + OQ**2)
    PS = np.sqrt(PQ**2 - QS**2)
    X = np.arctan(OQ/OP)
    Y = np.arctan(QS/PS)
    a1 = np.degrees(X) + np.degrees(Y)
    CD = PS
    Vc = Vb + r1*np.sin(np.radians(a1))
    Hc = r1*(1-np.cos(np.radians(a1)))
    MDc = Vb + (a1/build_rate_1)*100
    Vd = Vc + CD*np.cos(np.radians(a1))
    Hd = Hc + CD*np.sin(np.radians(a1))
    MDd = MDc + CD
    He = Hd + r2*(np.cos(np.radians(a2)) - np.cos(np.radians(a1)))
    MDe = MDd + (a1 - a2)*100/build_rate_2
    MDt = MDe + (Vt - Ve)/np.cos(np.radians(a2))

    p = st.sidebar.button('Show the Profile Trajectories')
    if p:
        st.sidebar.write(f'Calculated Radius (r1): {r1:.2f} ft')
        st.sidebar.write(f'Calculated Radius (r2): {r2:.2f} ft')
        st.sidebar.write(f'Calculated Inclination after Buildup: {a1:.2f}°')
        st.sidebar.write(f'Calculated Drop Angle: {a1 - a2:.2f}°')
        trajectory = {
           'Point': ['Start', 'Kick Off', 'End of Buildup', 'Start of Drop', 'End of Drop', 'Target'],
           'V(FT)': [0, Vb, Vc, Vd, Ve, Vt],
           'H(FT)': [0, 0, Hc, Hd, He, Ht],
           'MD(FT)': [0, Vb, MDc, MDd, MDe, MDt]
           }
        df = pd.DataFrame(trajectory)
        st.header('***The Profile trajectory is shown as below:***')
        st.table(df)

        MDx_values = np.linspace(0, MDt, 10000)
        Vx_values = []
        Hx_values = []
        a1_values = []
        drop_values = []

        for MDx in MDx_values:
            if MDx <= Vb:
                Vx = MDx
                Hx = 0
                a_1 = 0
                dr = 0
            elif MDx <= MDc:
                a_1 = (MDx - Vb)*build_rate_1/100
                dr = 0
                Vx = Vb + r1*np.sin(np.radians(a_1))
                Hx = r1*(1-np.cos(np.radians(a_1)))
            elif MDx <= MDd:
                CX = MDx - MDc
                Vx = Vc + CX*np.cos(np.radians(a1))
                Hx = Hc + CX*np.sin(np.radians(a1))
                a_1 = a1
                dr = 0
            elif MDx <= MDe:
                a_1 = a1
                a_2 = (MDx - MDd)*build_rate_2/100
                Vx = Vd + r2*(np.sin(np.radians(a1)) - np.sin(np.radians(a1 - a_2)))
                Hx = Hd + r2*(np.cos(np.radians(a1-a_2)) - np.cos(np.radians(a1)))
                dr = a_2
            else:
                EX = MDx - MDe
                Vx= Ve + EX*np.cos(np.radians(a2))
                Hx = He + EX*np.sin(np.radians(a2))
                a_1 = a1
                dr = a_2

            Vx_values.append(Vx)
            Hx_values.append(Hx)
            a1_values.append(a_1)
            drop_values.append(dr)
 
        plt.style.use('classic')
        fig, ax = plt.subplots()
        ax.plot(Hx_values,Vx_values , label='Build, Hold and Drop Trajectory')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Hx_values, y=Vx_values, mode='lines', name='Build, Hold and Drop Trajectory',
                         hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Buildup Inclination: %{customdata[1]}°<br>Drop Angle: %{customdata[2]}°', customdata=np.column_stack(((MDx_values, a1_values, drop_values))), line=dict(width= 4)))
        
        
        # st.pyplot(fig)
        fig.update_layout(
        title='Build, Hold and Drop Profile',
        xaxis_title='Horizontal Distance (ft)',
        yaxis_title='Vertical Depth (ft)',
        yaxis=dict(
        autorange='reversed'),
        hovermode='closest')
        st.plotly_chart(fig)

        # Display the data
        st.subheader('Buil, Hold and Drop Trajectory Data')
        st.write(pd.DataFrame({'Measured Depth (MD),ft': MDx_values, 'Vertical Depth (v), ft': Vx_values, 'Horizontal Distance (H), ft': Hx_values, ' Buildup Inclination Angle (°)' : a1_values, 'Drop Angle (°)': drop_values}))
