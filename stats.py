import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def qualitative_summary(df, cname):
    """
    Creates a qualitative summary, bar plot and pie chart of the column cname of the dataframe df.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe to be analyzed
    cname : string
        The name of the column to be analyzed

    """

    count = df[cname].value_counts()
    frequency = pd.DataFrame({cname: count.index, 'Frequency':count.values})
    frequency['Relative Frequency'] = frequency['Frequency']/frequency['Frequency'].sum()
    print("Numerical Summary of " + cname + "\n")
    print(frequency.set_index(cname))
    print("\n\n")

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    sns.barplot(x=cname, y='Frequency', data=frequency, ax=ax[0])
    ax[0].set_title("Frequency of " + cname)
    #rotate x-axis labels
    ax[0].set_xticklabels(ax[0].get_xticklabels(),rotation=45)

    ax[1].pie(frequency['Frequency'], labels=frequency[cname], autopct='%1.1f%%')
    ax[1].set_title("Relative Frequency of " + cname)

    plt.show()