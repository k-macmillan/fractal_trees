import seaborn as sns
import matplotlib.pyplot as plt

from natural.automata.reaction_diffusion import gray_scott

u, v = gray_scott(N=256, ru=0.16, rv=0.08, f=0.06, k=0.062, iters=3000)

sns.heatmap(u, square=True, xticklabels=False, yticklabels=False)
plt.show()
