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
    
    input_method = st.radio('**Please Select the Type of Drilling profile:**', ('Build and Hold Profile', 'Build, Hold and Drop Profile', 'Slanted Buildup Prfile', 'Horizontal Single Buildup Profile', 'Horizontal Double Buildup Profile'), index = None)

    if input_method == 'Build and Hold Profile':
        st.session_state.page = 'Build_Hold'
        st.rerun()
    elif input_method == 'Build, Hold and Drop Profile':
        st.session_state.page = 'Build_Hold_Drop'
        st.rerun()
    elif input_method == 'Slanted Buildup Prfile':
        st.session_state.page = 'Slanted'
        st.rerun()
    elif input_method == 'Horizontal Single Buildup Profile':
        st.session_state.page = 'Horizontal_Single'
        st.rerun()
    elif input_method == 'Horizontal Double Buildup Profile':
        st.session_state.page = 'Horizontal_Double'
        st.rerun()

elif st.session_state.page == 'Build_Hold':
    st.write('*It is used in the targets where a large horizontal displacement is required at relatively shallow depth. Shallow kick off point is selected. Under normal conditions, 15° - 55° inclination can be achieved. Although greater inclinations have been drilled in required cases.*')
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
        #ax.plot(Hx_values,Vx_values , label='Build and Hold Trajectory')
        
        # ax.set_xlabel('Horizontal Distance (ft)')
        # ax.set_ylabel('Vertical Depth (ft)')
        # ax.set_title('Build and Hold Profile')
        # ax.legend()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Hx_values, y=Vx_values, mode='lines', name='Trajectory',
                         hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Inclination: %{customdata[1]}°', customdata=np.column_stack((MDx_values, a_values)), line=dict(width= 4)))
        text_points = {
            'Hx': [0, 0, Hc, Ht],
            'Vx': [0, Vb, Vc, Vt],   # Example specific Hx points
            'MDx': [0, Vb, MDc, MDt],
            'A': [0, 0, a, a],
    
            'labels': ['Start', 'Kick Off', 'End of Build Up', 'Target']  # Labels for the specific points
            }
        fig.add_trace(go.Scatter(
            x=text_points['Hx'],
            y=text_points['Vx'],
            mode='markers+text',
            name= 'Corners',
            text=text_points['labels'],
            textposition='top right',  # Adjust text position as needed
            marker=dict(color='red', size=7, symbol='circle'),
            hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Inclination: %{customdata[1]}°<br>Label: %{text}', customdata=np.column_stack((text_points['MDx'], text_points['A'])), line=dict(width= 4)))  # Disable hover for these markers))

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
    st.write('*It is used in the targets where a smaller horizontal displacement is required at relatively deep vertical depth as compared to type-1 profile. In first build upattempt, the required inclination is achieved. Then the well is drilled tangentially for constant inclination and while approaching the pay zone the inclination is drop out so that the target can be penetrated.*')
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
        #ax.plot(Hx_values,Vx_values , label='Build, Hold & Drop Trajectory')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Hx_values, y=Vx_values, mode='lines', name='Trajectory',
                         hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Buildup Inclination: %{customdata[1]}°<br>Drop Angle: %{customdata[2]}°', customdata=np.column_stack(((MDx_values, a1_values, drop_values))), line=dict(width= 4)))
        text_points = {
            'Hx': [0, 0, Hc, Hd, He, Ht],
            'Vx': [0, Vb, Vc, Vd, Ve, Vt],   # Example specific Hx points
            'MDx': [0, Vb, MDc, MDd, MDe, MDt],
            'A': [0, 0, a1, a1, a1, a1],
            'D': [0, 0, 0, 0, dr, dr],
            'labels': ['Start', 'Kick Off', 'End of Build Up', 'Start of Drop', 'End of Drop', 'Target']  # Labels for the specific points
            }
        fig.add_trace(go.Scatter(
            x=text_points['Hx'],
            y=text_points['Vx'],
            mode='markers+text',
            name= 'Corners',
            text=text_points['labels'],
            textposition='top right',  # Adjust text position as needed
            marker=dict(color='red', size=7, symbol='circle'),
            hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Buildup Inclination: %{customdata[1]}°<br>Drop Angle: %{customdata[2]}°<br>Label: %{text}', customdata=np.column_stack(((text_points['MDx'], text_points['A'], text_points['D']))), line=dict(width= 4)))  # Disable hover for these markers
            
        
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

elif st.session_state.page == 'Slanted':
    st.write('*This type of profile can be drilled using the slanted rig that provides initial inclination at the time of spudding of the well profile by slanted position of the rig at the surface. This profile is beneficial to provide extension in the horizontal displacement, and is useful to penetrate the targets located at a far distances which are unable to be drilled by conventional well profile.*')
    st.sidebar.title('Enter the known Parameters required')
    MDb = st.sidebar.number_input('Enter KOP Measured Depth (ft)', value=1000.0, min_value=0.0, step = 0.01)
    Vt = st.sidebar.number_input('Enter TVD of Target (ft)', value=10000.0, min_value=0.0, step = 0.01)
    Ht = st.sidebar.number_input('Enter Horizontal Distance to Target (ft)', value=12000.0, min_value=0.0, step = 0.01)
    a1 = st.sidebar.number_input('Enter the inclination angle at Start (degrees): ', value=30.0, min_value=0.0, step=0.01)
    build_rate = st.sidebar.number_input('Enter Build Rate (degrees per 100 ft)', value=1.5, min_value=0.0, step = 0.01)
    # Calculations
    def radius_of_curvature(build_rate):
        return 18000 / (np.pi * build_rate)
    r1 = radius_of_curvature(build_rate)

    NT = Ht - Vt*np.tan(np.radians(a1))
    QT = NT *np.cos(np.radians(a1))
    NQ = NT *np.sin(np.radians(a1))
    AN = Vt/(np.cos(np.radians(a1)))
    AQ = AN + NQ
    X = np.arctan((QT - r1)/(AQ - MDb))
    Y = np.arcsin((r1*np.cos(X))/(AQ - MDb))
    a2 = np.degrees(X) + np.degrees(Y)
    at = a1 + a2
    CM = r1*(1-np.cos(np.radians(a2)))/(np.cos(np.radians(a1)))
    AD = MDb + r1*np.sin(np.radians(a2))
    DM = r1*(1- np.cos(np.radians(a2)))*np.tan(np.radians(a1))
    AM = AD - DM
    # Corner Points
    Vb = MDb*np.cos(np.radians(a1))
    Hb = MDb*np.sin(np.radians(a1))
    Vc = AM*np.cos(np.radians(a1))
    Hc = AM*np.sin(np.radians(a1)) + CM
    MDc = MDb + a2*100/build_rate
    MDt = MDc + (Vt-Vc)/np.cos(np.radians(at))

    s = st.sidebar.button('Show the Profile Trajectories')
    if s:
        st.sidebar.write(f'Calculated Radius (r): {r1:.2f} ft')
        st.sidebar.write(f'Calculated Inclination Buildup Angle: {a2:.2f}°')
        st.sidebar.write(f'Calculated Total Inclination Angle: {at:.2f}°')
        trajectory = {
            'Point': ['Start', 'Kick Off', 'End of Build-Up', 'Target'],
            'V(FT)': [0, Vb, Vc, Vt],
            'H(FT)': [0, 0, Hc, Ht],
            'MD(FT)': [0, Vb, MDc,MDt]
        }
        df = pd.DataFrame(trajectory)
        st.header('***The Profile trajectory is shown as below:***')
        st.table(df)

        MDx_values = np.linspace(0, MDt, 500)
        Vx_values = []
        Hx_values = []
        a2_values = []
        at_values =[]


        for MDx in MDx_values:


            if MDx <= MDb:
                Vx = MDx*np.cos(np.radians(a1))
                Hx = MDx*np.sin(np.radians(a1))
                a2x = 0
                atx = a1 + a2x
            elif MDx <= MDc:
                a_2 = (MDx - MDb)*build_rate/100
                a2x =a_2
                atx = a1 + a2x
                CMx = r1*(1-np.cos(np.radians(a_2)))/(np.cos(np.radians(a1)))
                ADx = MDb + r1*np.sin(np.radians(a_2))
                DMx = r1*(1- np.cos(np.radians(a_2)))*np.tan(np.radians(a1))
                AMx = ADx - DMx

                Vx = AMx*np.cos(np.radians(a1))
                Hx = AMx*np.sin(np.radians(a1)) + CMx
            else:
                CX = MDx - MDc
                Vx = Vc + CX*np.cos(np.radians(at))
                Hx = Hc + CX*np.sin(np.radians(at))
                a2x = a2
                atx = a1 + a2x

            Vx_values.append(Vx)
            Hx_values.append(Hx)
            a2_values.append(a2x)
            at_values.append(atx)
        
        fig, ax = plt.subplots()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Hx_values, y=Vx_values, mode='lines', name='Trajectory',
                         hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Inclination Buildup: %{customdata[1]}°<br>Total Inclination Angle: %{customdata[2]}°', customdata=np.column_stack(((MDx_values, a2_values, at_values))), line=dict(width= 4)))
        text_points = {
            'Hx': [0, Hb, Hc, Ht],
            'Vx': [0, Vb, Vc, Vt],   # Example specific Hx points
            'MDx': [0, MDb, MDc, MDt],
            'A2': [0, 0, a2, a2],
            'AT': [0, a1, at, at],
    
            'labels': ['Start', 'Kick Off', 'End of Build Up', 'Target']  # Labels for the specific points
            }
        fig.add_trace(go.Scatter(
            x=text_points['Hx'],
            y=text_points['Vx'],
            mode='markers+text',
            name= 'Corners',
            text=text_points['labels'],
            textposition='top right',  # Adjust text position as needed
            marker=dict(color='red', size=7, symbol='circle'),
            hovertemplate='MD: %{customdata[0]}<br>H: %{x}<br>V: %{y}<br>Inclination Buildup: %{customdata[1]}°<br>Total Inclination Angle: %{customdata[2]}°<br>Label: %{text}', customdata=np.column_stack(((text_points['MDx'], text_points['A2'], text_points['AT']))), line=dict(width= 4)))  # Disable hover for these markers))

        # st.pyplot(fig)
        fig.update_layout(
        title='Slanted Buildup Profile',
        xaxis_title='Horizontal Distance (ft)',
        yaxis_title='Vertical Depth (ft)',
        yaxis=dict(
        autorange='reversed'),
        hovermode='closest')
        st.plotly_chart(fig)

        # Display the data
        st.subheader('Slanted Buildup Profile Trajectory Data')
        st.write(pd.DataFrame({'Measured Depth (MD),ft': MDx_values, 'Vertical Depth (v), ft': Vx_values, 'Horizontal Distance (H), ft': Hx_values, 'Inclination Buildup Angle (°)' : a2_values, 'Total Inclination Angle (°)': at_values}))


