import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.optimize import curve_fit

# Function to fit data to decline models
def fit_decline_model(t, q, model_func, p0):
    params, _ = curve_fit(model_func, t, q, p0=p0)
    return params

# Function to define decline curve models
def exponential_decline(t, qi, di):
    return qi * np.exp(-di * t)

def hyperbolic_decline(t, qi, di, b):
    return qi / ((1 + b * di * t) ** (1 / b))

def harmonic_decline(t, qi, di):
    return qi / (1 + di * t)

# Define the cumulative production functions
def cumulative_exponential(qi,di,t):
    return (qi/di)*(1-np.exp(-di*t))
def cumulative_hyperbolic(qi,di,b,t):
    if b ==0:
        return cumulative_exponential(qi,di,t)
    return (qi / ((1 - b) * di)) * (1 - (1 / ((1 + b * di * t) ** ((1 - b) / b))))
def cumulative_harmonic(qi,di,t):
    return (qi/di)*(np.log(1+di*t))

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

#def main():
    # Add "Home" button
if st.session_state.page != 'home':
    if st.sidebar.button('Home'):
        st.session_state.page = 'home'
        # st.experimental_rerun()

if st.session_state.page == 'home':
    # Initial interface with title and description
    st.markdown("<h1 style='text-align: center; font-size: 50px;text-decoration: underline; margin-bottom: 0; color: blue;'>Decline Curve Analysis</h1>", unsafe_allow_html=True)
    st.markdown("**<p style='text-align: center; font-size: 20px; margin-top: 0; color: red;'>(History Matching & Production Forecast)</p>**", unsafe_allow_html=True)
    st.markdown("*Welcome to the Advanced Decline Curve Analysis & Production Forecasting tool! This application leverages the power of Exponential, Hyperbolic, and Harmonic decline models to provide comprehensive reservoir performance analysis and future production forecasting. Whether you have existing flow rate vs. time data or prefer to input parameters manually, our intuitive interface and advanced algorithms ensure accurate and insightful results to aid in your reservoir management and decision-making processes.*")

    # Click Input options
    input_method = st.radio('Please select the operation you would like to perform.', ('Input Parameters', 'Upload CSV File'), index = None)

    if input_method == 'Input Parameters':
        st.session_state.page = 'input_parameters'
        # elif input_method == 'Upload CSV File':
        #     st.session_state.page = 'upload_csv'
        st.experimental_rerun()
    elif input_method == 'Upload CSV File':
        st.session_state.page = 'upload_csv'
        st.experimental_rerun()

elif st.session_state.page == 'input_parameters':
        
        st.sidebar.title('Enter Parameters for Decline Curve Analysis')

        # Sidebar inputs for parameters
        qi = st.sidebar.number_input('Initial Production Rate (qi)', value=1000, min_value=0)
        di = st.sidebar.number_input('Decline Rate (di)', value=0.1, min_value=0.0)
        b = st.sidebar.number_input('Hyperbolic Decline Constant (b)', value=0.5, min_value=0.0)
        time_period = st.sidebar.number_input('Time Period (years)', value=10, min_value=1, step=1)
        

        # Generate time data
        t = np.linspace(0, time_period, 100)

    # Calculate production rates using each method
        exp_production = exponential_decline(t, qi, di)
        hyp_production = hyperbolic_decline(t, qi, di, b)
        har_production = harmonic_decline(t, qi, di)

    # Calculate cumulative production using each method
        exp_cumulative = cumulative_exponential(qi, di, t)
        hyp_cumulative = cumulative_hyperbolic(qi, di, b, t)
        har_cumulative = cumulative_harmonic(qi, di, t)
    #show button
        b = st.button('Show Reservoir Performance Analysis')
        if b:
        # New title and headers
            st.header('Different Decline Curve Models have been analyzed as follows below:')
    # Plotting production rates
            fig, ax = plt.subplots()
            fig = go.Figure()
            #ax.plot(t, exp_production, label='Exponential Decline')
            fig.add_trace(go.Scatter(x=t, y= exp_production, mode='lines+markers', name='Exponential Decline'))
            #ax.plot(t, hyp_production, label='Hyperbolic Decline')
            fig.add_trace(go.Scatter(x=t, y=hyp_production, mode='lines+markers', name='Hyperbolic Decline'))
            #ax.plot(t, har_production, label='Harmonic Decline')
            fig.add_trace(go.Scatter(x=t, y=har_production, mode='lines+markers', name='Harmonic Decline'))

            #ax.set_xlabel('Time (years)')
            #ax.set_ylabel('Production Rate')
            #ax.set_title('Decline Curve Analysis')
            #ax.legend()
            fig.update_layout(
                title='Decline Curve Analysis',
                xaxis_title='Time (years)',
                yaxis_title='Production Rate (q)',
                hovermode='x unified',
                width = 1500,
                height = 500
            )

            #st.pyplot(fig)
            st.plotly_chart(fig)

    # Plotting cumulative production
            fig2, ax2 = plt.subplots()
            fig2 = go.Figure()
            #ax2.plot(t, exp_cumulative, label='Exponential Cumulative Production')
            fig2.add_trace(go.Scatter(x=t, y=exp_cumulative, mode = 'lines+markers', name= 'Exponential Cumulative Production'))
            #ax2.plot(t, hyp_cumulative, label='Hyperbolic Cumulative Production')
            fig2.add_trace(go.Scatter(x=t, y=hyp_cumulative, mode = 'lines+markers', name= 'Hyperbolic Cumulative Production'))
            #ax2.plot(t, har_cumulative, label='Harmonic Cumulative Production')
            fig2.add_trace(go.Scatter(x=t, y=har_cumulative, mode = 'lines+markers', name= 'Harmonic Cumulative Production'))

            #ax2.set_xlabel('Time (years)')
            #ax2.set_ylabel('Cumulative Production')
            #ax2.set_title('Cumulative Production Analysis')
            #ax2.legend()
            fig2.update_layout(
                title='Cumulative Production Analysis',
                xaxis_title='Time (years)',
                yaxis_title='Cumulative Production',
                hovermode='x unified',
                width = 1500,
                height = 500
            )

            #st.pyplot(fig2)
            st.plotly_chart(fig2)
            # Display the data
            st.subheader('Decline Curve Data')
            st.write('### Exponential Decline')
            st.write(pd.DataFrame({'Time (years)': t, 'Production Rate': exp_production, 'Cumulative Production': exp_cumulative}))

            st.write('### Hyperbolic Decline')
            st.write(pd.DataFrame({'Time (years)': t, 'Production Rate': hyp_production, 'Cumulative Production': hyp_cumulative}))

            st.write('### Harmonic Decline')
            st.write(pd.DataFrame({'Time (years)': t, 'Production Rate': har_production, 'Cumulative Production': har_cumulative}))

elif st.session_state.page == 'upload_csv':
    uploaded_file = st.file_uploader("Upload your 'time|rate' CSV file  \n*(#Uploaded file should contain first column titled as time and next as rate.)*", type=["csv"])
    if uploaded_file is not None:
        # Define a new future time range for the forecast
        #future_time_period = st.sidebar.number_input('Forecast Time Period (years)', value=10, min_value=1, step=1)
        
        #p = st.button('Show Best Fit Model')

        #if p:
            
        st.header('The Best Fit Model is shown as follows:')
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(data.head())

            # Assume the file has columns 'time' and 'rate'
        t = data['time'].values
        q = data['rate'].values

            # Fit the data to each model
        exp_params = fit_decline_model(t, q, exponential_decline, p0=[q[0], 0.1])
        har_params = fit_decline_model(t, q, harmonic_decline, p0=[q[0], 0.1])
        hyp_params = fit_decline_model(t, q, hyperbolic_decline, p0=[q[0], 0.1, 0.5])

            # Calculate R-squared for each model
        exp_residuals = q - exponential_decline(t, *exp_params)
        exp_ss_res = np.sum(exp_residuals**2)
        exp_ss_tot = np.sum((q - np.mean(q))**2)
        exp_r2 = 1 - (exp_ss_res / exp_ss_tot)

        har_residuals = q - harmonic_decline(t, *har_params)
        har_ss_res = np.sum(har_residuals**2)
        har_ss_tot = np.sum((q - np.mean(q))**2)
        har_r2 = 1 - (har_ss_res / har_ss_tot)

        hyp_residuals = q - hyperbolic_decline(t, *hyp_params)
        hyp_ss_res = np.sum(hyp_residuals**2)
        hyp_ss_tot = np.sum((q - np.mean(q))**2)
        hyp_r2 = 1 - (hyp_ss_res / hyp_ss_tot)

            # Determine the best fit model
        r2_values = {'Exponential': exp_r2, 'Harmonic': har_r2, 'Hyperbolic': hyp_r2}
        best_fit = max(r2_values, key=r2_values.get)

        st.write(f"Best fit model: {best_fit}")

        #future_t = np.linspace(t[-1], t[-1] + future_time_period, 100)

        if best_fit == 'Exponential':
            qi, di = exp_params
            best_production = exponential_decline(t, qi, di)
            best_cumulative = cumulative_exponential(qi, di, t)
            st.write(f"Calculated decline rate (Di): {di:.2f}")
            #forecast_production = exponential_decline(future_t, qi, di)
            #forecast_cumulative = cumulative_exponential(qi, di, future_t)
                
        elif best_fit == 'Harmonic':
            qi, di = har_params
            best_production = harmonic_decline(t, qi, di)
            best_cumulative = cumulative_harmonic(qi, di, t)
            st.write(f"Calculated decline rate (Di): {di:.2f}")
            #forecast_production = harmonic_decline(future_t, qi, di)
            #forecast_cumulative = cumulative_harmonic(qi, di, future_t)
        else:
            qi, di, b = hyp_params
            best_production = hyperbolic_decline(t, qi, di, b)
            best_cumulative = cumulative_hyperbolic(qi, di, b, t)
            st.write(f"Calculated decline rate (Di): {di:.2f}")
            st.write(f"Calculated b factor: {b:.2f}")
            #forecast_production = hyperbolic_decline(future_t, qi, di, b)
            #forecast_cumulative = cumulative_hyperbolic(qi, di, b, future_t)

        # Define a new future time range for the forecast
        future_time_period = st.sidebar.number_input('Forecast Time Period (years)', value=10, min_value=1, step=1)
        p = st.sidebar.button('Show Production Forecast')
        if p:
            future_t = np.linspace(t[-1], t[-1] + future_time_period, 100)
            if best_fit == 'Exponential':
                forecast_production = exponential_decline(future_t, qi, di)
                forecast_cumulative = cumulative_exponential(qi, di, future_t)
            elif best_fit == 'Harmonic':
                forecast_production = harmonic_decline(future_t, qi, di)
                forecast_cumulative = cumulative_harmonic(qi, di, future_t)
            else:
                forecast_production = hyperbolic_decline(future_t, qi, di, b)
                forecast_cumulative = cumulative_hyperbolic(qi, di, b, future_t)

            # Plotting best fit model production rates
            fig, ax = plt.subplots()
            fig = go.Figure()
            ax.plot(t, q, 'o', label='Data')
            #ax.plot(t, best_production, label=f'Best Fit: {best_fit} Decline')
            fig.add_trace(go.Scatter(x=t, y=best_production, mode='lines+markers', name= f'Best Fit: {best_fit} Decline'))
            #ax.plot(future_t, forecast_production, label=f'Forecast: {best_fit} Decline', linestyle='--')
            fig.add_trace(go.Scatter(x=future_t, y=forecast_production, mode='lines+markers', name= f'Forecast: {best_fit} Decline'))

                #ax.set_xlabel('Time (years)')
                #ax.set_ylabel('Production Rate')
                #ax.set_title('Best Fit Decline Curve Analysis with Forecast')
                #ax.legend()
            fig.update_layout(
                title='Best Fit Decline Curve Analysis with Forecast',
                xaxis_title='Time (years)',
                yaxis_title='Production Rate (q)',
                hovermode='x unified',
                width = 1500,
                height = 500)

                #st.pyplot(fig)
            st.plotly_chart(fig)

                # Plotting best fit model cumulative production
            fig2, ax2 = plt.subplots()
            fig2= go.Figure()
            #ax2.plot(t, best_cumulative, label=f'Best Fit: {best_fit} Cumulative Production')
            fig2.add_trace(go.Scatter(x=t, y=best_cumulative, mode='lines+markers', name= f'Best Fit: {best_fit} Cumulative Production'))
            #ax2.plot(future_t, forecast_cumulative, label=f'Forecast: {best_fit} Cumulative Production', linestyle='--')
            fig2.add_trace(go.Scatter(x=future_t, y=forecast_cumulative, mode='lines+markers', name= f'Forecast: {best_fit} Cumulative Production'))

                #ax2.set_xlabel('Time (years)')
                #ax2.set_ylabel('Cumulative Production')
                #ax2.set_title('Best Fit Cumulative Production Analysis with Forecast')
                #ax2.legend()
            fig2.update_layout(
                title='Best Fit Cumulative Production Analysis with Forecast',
                xaxis_title='Time (years)',
                yaxis_title='Cumulative Production',
                hovermode='x unified',
                width = 1500,
                height = 500)

                #st.pyplot(fig2)
            st.plotly_chart(fig2)

                 # Display the best fit model data
            st.subheader('Best Fit Decline Curve Data')
            st.write(f'### {best_fit} Decline')
            st.write(pd.DataFrame({'Time (years)': t, 'Production Rate': best_production, 'Cumulative Production': best_cumulative}))

                # Display the forecast data
            st.subheader('Production Forecast Data')
            st.write(pd.DataFrame({'Future Time (years)': future_t, 'Forecast Production Rate': forecast_production}))

                # Display the forecast cumulative production data
            st.subheader('Cumulative Production Forecast Data')
            st.write(pd.DataFrame({'Future Time (years)': future_t, 'Forecast Cumulative Production': forecast_cumulative}))



