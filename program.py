import numpy as np, matplotlib.pyplot as plt, seaborn as sns, mpld3
%matplotlib inline
sns.set_context("poster")
sns.set_style('whitegrid')

plt.plot([3,1,4,1,5,9,6,2], 'o-')
plt.title('Hello, World')
mpld3.save_json(plt.gcf(), 'test.json')
