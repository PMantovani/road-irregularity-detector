import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.01, 20.0, 0.01)
c = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
# f1_3 = [0.8166, 0.84788, 0.84242, 0.862646, 0.92025, 0.91640, 0.9062379, 0.87707] # macro-average
f1_2 = [0.85227, 0.87302, 0.87252, 0.89044, 0.93160, 0.93835, 0.941134, 0.93522] # macro-average

# log x axis
csfont = {'fontname':'Calibri'}
plt.semilogx(c, f1_2)
plt.xlabel(r'$Par\hat{a}metro\: C$', **csfont)
plt.ylabel('F1 Score', **csfont)
plt.grid(True)
plt.show()
# plt.savefig('C:\\Users\\pmant\\Desktop\\destination_path.pdf', format='pdf', dpi=1000)