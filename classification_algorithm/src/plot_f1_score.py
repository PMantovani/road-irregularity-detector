import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.01, 20.0, 0.01)
c = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
f1 = [78.35, 82.78, 82.18, 84.84, 91.59, 91.26, 90.17, 87.07]

# log x axis
plt.semilogx(c, f1)
plt.title('Classificador Linear')
plt.xlabel('Parametro C')
plt.ylabel('F1 Score')
plt.grid(True)
plt.show()