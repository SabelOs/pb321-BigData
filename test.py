#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

a = np.linspace(0,100)
b = np.exp(a)

plt.figure()
plt.loglog(a,b)
plt.show()



# %%
