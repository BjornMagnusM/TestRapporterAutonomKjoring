import control as ctl
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.linalg import expm
# Define the transfer function
numerator = [4.308, 101.2, 141.5]
denominator = [1, 11.02, 133.8, 142]
# numerator = [4.014, 83.39, 2173]
# denominator = [1, 31.09, 357.9, 2170]
# numerator = [3.75, 61.48, 2546]
# denominator = [1, 38.65, 519.6, 2533]
# numerator = [3.606, 40.12, 1421]
# denominator = [1, 16.98, 273.3, 1411]


# Display the state-space matrices
dt = 0.01  # Time step (seconds)
t_end = 6  # End time (seconds)
t_array = np.arange(0, t_end, dt) #list with all the times 
input_signal = [] #innit for input signal

# Convert the transfer function to state-space representation
ss = ctl.tf2ss(numerator,denominator)
ss= ctl.c2d(ss,dt,"zoh")
print(ss)
A = ss.A
B = ss.B
C = ss.C
D = ss.D

A_d = np.array([[0.8894027, -1.2312131, -1.3414861],
              [0.0094466, 0.9922662, -0.0068527],
              [0.0000481, 0.0097549, 0.9999758]])

B_d = np.array([[0.0094466],
              [0.0000481],
              [0.0000005]])

C_d =np.array([[4.308, 101.2, 141.5]])

D_d = np.array([[0]])



x = np.zeros((A.shape[0],))
x_d = np.zeros((A.shape[0],))



for t in range(0, len(t_array), 1):
    if t < 100: input_signal.append(0)
    else: input_signal.append(0.6)

# Initialize output storage
output_signal = []
output_signal_d = []
# Real-time simulation loop
for u in input_signal:
    # State update equation: x(k+1) = Ax(k) + Bu(k)
    x = np.dot(A, x) + np.dot(B, u)  # Directly update for discrete system, no dt multiplication
    x_d = np.dot(A_d, x_d) + np.dot(B_d, u)
    # Output equation: y(k) = Cx(k) + Du(k)
    y = np.dot(C, x) + D * u
    y_d = np.dot(C_d, x_d) + D_d * u
    output_signal.append(y[0][0])  # Assuming y_disc is scalar
    output_signal_d.append(y_d[0][0])


#plots data 
matplotlib.rcParams.update({'font.size': 20})
plt.figure(figsize=(10, 6))
plt.plot(t_array, input_signal, label='Ingangs signal')
plt.plot(t_array, output_signal, label='Utgangs signal diskretisert med python', linestyle='--')
plt.plot(t_array, output_signal_d, label='Utgangs signal diskretisert manuelt', linestyle='--')
plt.title('Steg respons Hiv')
plt.xlabel('Tid (sekkunder)')
plt.ylabel('Signal Verdi')
plt.legend()
plt.grid(True)
plt.show()




# B = np.array([[1],
#               [0],
#               [0]])
# T = 0.01  # Sampling period

# # Compute A_d using matrix exponential
# A_d = expm(A * T)

# # Identity matrix of the same size as A
# I = np.eye(A.shape[0])

# # Compute B_d using the formula B_d = A^(-1)(A_d - I)B
# B_d = np.linalg.inv(A).dot(A_d - I).dot(B)

# print("Discrete B matrix (B_d):")
# print(B_d)


# # Example list of values
# values = output_signal
# # Convert the list to a DataFrame
# df = pd.DataFrame(values, columns=['Values'])

# # Specify the file path to save the Excel file (change 'output.xlsx' to your desired file name)
# file_path = 'output.xlsx'

# # Write the DataFrame to an Excel file
# df.to_excel(file_path, index=False)