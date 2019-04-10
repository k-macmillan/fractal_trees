"""Python module implementing fractals and cellular automata."""
import matplotlib as mpl

# Apparently, SNS stands for "Samuel Norman Seaborn", a fictional
# character from The West Wing
import seaborn as sns

sns.set()
# Increase default figure size and DPI
scale = 1.8
mpl.rcParams["figure.figsize"] = (scale * 6, scale * 4)
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.bbox"] = "tight"
