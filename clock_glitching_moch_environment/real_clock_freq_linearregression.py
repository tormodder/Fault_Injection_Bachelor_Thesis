# Live plot code
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from scipy import stats

# Linear Regression for the real clock frequency
# with open('./real_clock_data/exported_clock.csv', 'r') as real_clock_data:
with open('./real_clock_data/exported_clock_glitched.csv', 'r') as real_clock_data:
    csv_reader = csv.reader(real_clock_data)
    x = []
    y = []
    for i, line in enumerate(csv_reader):
        x.append(i)
        y.append(float(line[0]))
    # print(x)
    # print(y)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print(f'Slope: {slope}, Intercept: {intercept}, R-value: {r_value}, P-value: {p_value}, Std-err: {std_err}')