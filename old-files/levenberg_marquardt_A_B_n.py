import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Experimental data of strain and stress
strain = np.array([0.0000000, 0.0002500, 0.0005000, 0.0007500, 0.0010000, 0.0012500, 0.0015007, 0.0017578, 0.0020620, 0.0026379, 0.0027346])
stress = np.array([0.0, 7.0, 14.0, 21.0, 28.0, 35.0, 42.0, 49.0, 56.0, 63.0, 63.692])

# Define the Ludwik function for fitting
def ludwik_model(epsilon, A, B, n):
    return A + B * epsilon**n

# Fit parameters using the Levenberg-Marquardt algorithm
parameters, _ = curve_fit(ludwik_model, strain, stress)

# Adjusted parameters
A, B, n = parameters
print(f"A = {A:.2f} MPa, B = {B:.2f} MPa, n = {n:.2f}")

# Calculate the fitted stress with the found parameters
fitted_stress = ludwik_model(strain, A, B, n)

# Plot the experimental data and the fit
p1, = plt.plot(strain, stress, 'o', label='Experimental data')
p2, = plt.plot(strain, fitted_stress, '-', label='Fit with Levenberg-Marquardt')

# First legend
legend1 = plt.legend(handles=[p1, p2], loc='upper left')

# Adjust the position of the text with parameters A, B, and n
plt.text(0.0015, 10, f"A = {A:.2f} MPa\nB = {B:.2f} MPa\nn = {n:.2f}", 
         fontsize=10, color='black', bbox=dict(facecolor='white', alpha=0.5))

# Additional plot settings
plt.xlabel('Strain (ε)')
plt.ylabel('Stress (σ) in MPa')
plt.title('Stress-Strain Curve Fit')
plt.show()
