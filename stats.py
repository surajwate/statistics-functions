import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

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


def two_var_qualitative(df, var1, var2):
    """
    Create bar plots equal to the number of unique values of var1, each of which shows the relative frequency of var2 for a unique value of var1.
    
    Parameters
    ----------
    df : pandas dataframe
        The dataframe to be analyzed
    var1 : string
        The name of the first column to be analyzed
    var2 : string
        The name of the second column to be analyzed

    """
    order = df[var2].unique().tolist()
    number_of_plots = df[var1].nunique()

    fig, ax = plt.subplots(nrows=1, ncols=number_of_plots, figsize=(12, 5))

    for i in range(number_of_plots):
        sdf = df[df[var1] == df[var1].unique()[i]]
        count = sdf[var2].value_counts()
        sns.barplot(x=count.index, y=count.values, ax=ax[i], order=order)
        ax[i].set_xticklabels(ax[i].get_xticklabels(),rotation=45)
        ax[i].title.set_text(f"Relative Frequency of {var2} for {var1} = {df[var1].unique()[i]}")

    plt.show()


def dotplot(df, var):
    """
    Create a dotplot of the column var of the dataframe df.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe to be analyzed
    var : string
        The name of the column to be analyzed

    """
    # Count the frequency of each unique value in the column var
    data_counts = Counter(df[var])

    # Separate the values and their frequencies
    values = list(data_counts.keys())
    counts = list(data_counts.values())

    # Create a dotplot
    plt.figure(figsize=(10, 2))  # Set the size of the figure

    for i in range(len(values)):
        x = [values[i]] * counts[i] # Create a list of values[i] repeated counts[i] times
        y = list(range(1, counts[i] + 1)) # Create a list from 1 to counts[i]
        plt.scatter(x, y)

    # Add labels and title
    plt.xlabel(var)
    plt.title(f'Dotplot of {var}')

    # Customize x-axis ticks
    plt.xticks(np.arange(min(values), max(values)))

    # Customize y-axis ticks
    plt.yticks(range(0, max(counts) + 2))
    plt.yticks([]) # Hide the y-axis ticks

    plt.tight_layout()
    plt.show()
