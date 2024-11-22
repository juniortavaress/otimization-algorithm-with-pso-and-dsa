import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Simulated data for strain rate (replace with actual data when available)
strain_rate = np.array([1, 10, 100, 1000, 10000])  # taxas de deformação [1/s]
flow_stress = np.array([50, 80, 120, 160, 190])    # tensões de escoamento [MPa]

# Define the JC model's strain rate hardening function
def jc_strain_rate_model(strain_rate, C):
    return flow_stress[0] * (1 + C * np.log(strain_rate / strain_rate[0]))

# Fit parameter C using the Levenberg-Marquardt algorithm
parameters, _ = curve_fit(jc_strain_rate_model, strain_rate, flow_stress)
C = parameters[0]
print(f"C = {C:.2f}")

# Calculate the fitted flow stress with the found parameter C
fitted_flow_stress = jc_strain_rate_model(strain_rate, C)

# Plot the experimental data and the fit
p1, = plt.plot(strain_rate, flow_stress, 'o', label='Experimental data')
p2, = plt.plot(strain_rate, fitted_flow_stress, '-', label='Fit with Levenberg-Marquardt')

# First legend
legend1 = plt.legend(handles=[p1, p2], loc='upper left')

# Adjust the position of the text with parameter C
plt.text(1000, 70, f"C = {C:.2f}", 
         fontsize=10, color='black', bbox=dict(facecolor='white', alpha=0.5))

# Additional plot settings
plt.xlabel('Strain Rate (ε˙) in 1/s')
plt.ylabel('Flow Stress (σ) in MPa')
plt.title('Flow Stress vs Strain Rate Curve Fit')
plt.xscale('log')  # Use a logarithmic scale for strain rate
plt.show()
