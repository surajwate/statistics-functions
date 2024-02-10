import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from tabulate import tabulate

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



def histogram_overlap(df, target, var, num_bins=10):
    """
    Create a histogram of the column var of the dataframe df for each unique value of the column target.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe to be analyzed
    target : string
        The name of the column to be analyzed
    var : string
        The name of the column to be analyzed
    num_bins : int
        The number of bins to be used in the histogram

    """
    # Create a list of unique values in the column target
    target_values = df[target].unique()

    # Create a histogram for each unique value of the column target
    for value in target_values:
        plt.hist(df[df[target] == value][var], bins=num_bins, alpha=0.5, label=str(value))

    # Add labels and title
    plt.xlabel(var)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {var} for each unique value of {target}')
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


def histogram_sidebyside(df, target, var, num_bins=10):
    """
    Create a side by side histograms of the column var of the dataframe df for each unique value of the column target.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe to be analyzed
    target : string
        The name of the target column to be analyzed (categorical variable)
    var : string
        The name of the variable column to be analyzed
    num_bins : int
        The number of bins to be used in the histogram

    """
    # Separate data by roles
    categories = df[target].unique()
    category_data = {cat: df[df[target] == cat][var] for cat in categories}

    # Determine the maximum range of values between roles
    max_range = max(max(values) for values in category_data.values()) - min(min(values) for values in category_data.values())

    # Calculate the bin width based on the desired number of bins
    bin_width = max_range / num_bins

    # Create bins
    bins = [i * bin_width + min(min(values) for values in category_data.values()) for i in range(num_bins + 1)]

    # Create subplots with a shared y-axis
    num_roles = len(categories)
    fig, axes = plt.subplots(nrows=1, ncols=num_roles, figsize=(12, 5), sharey=True)

    for i, cat in enumerate(categories):
        ax = axes[i]
        ax.hist(category_data[cat], bins=bins, alpha=0.5, label=str(cat))
        ax.set_xlabel(var)
        ax.set_ylabel('Frequency')
        ax.set_title(f'Histogram of {var} for {target} = {cat}')

    plt.tight_layout()
    plt.show()


def numerical_summary(df, cname):
    """
    Creates a detailed numerical summary of the column cname of the dataframe df.
    Includes additional statistics and a box plot alongside the histogram.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe to be analyzed
    cname : string
        The name of the column to be analyzed
    """

    print(f"Summary Statistics for {cname}\n" + "-"*40)
    
    # Extract the column data
    data = df[cname]

    # Calculate statistics
    median = data.median()
    mean = data.mean()
    std = data.std()
    min_val = data.min()
    max_val = data.max()
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    skewness = data.skew()

    # Create a summary table
    summary_table = [
        ['Mean', mean],
        ['Median', median],
        ['Standard Deviation', std],
        ['Minimum', min_val],
        ['25th Percentile', q1],
        ['75th Percentile', q3],
        ['Interquartile Range', iqr],
        ['Maximum', max_val],
        ['Skewness', skewness]
    ]

    # Define table headers
    headers = ['Measure', 'Value']

    # Print the summary table
    print(tabulate(summary_table, headers, tablefmt="fancy_grid"))

    # Create a figure with subplots
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    # Histogram with KDE
    sns.histplot(data, kde=True, ax=ax[0])
    ax[0].axvline(median, color='violet', linestyle='dashed', linewidth=1.25, label='Median')
    ax[0].axvline(mean, color='blue', linestyle='dashed', linewidth=1.25, label='Mean')

    # Draw standard deviation lines
    ax[0].axvline(mean + std, color='darkgreen', linestyle='dashed', linewidth=1, label='1 Std Dev')
    ax[0].axvline(mean - std, color='darkgreen', linestyle='dashed', linewidth=1)

    ax[0].axvline(mean + (2* std), color='lime', linestyle='dashed', linewidth=0.75, label='2 Std Dev')
    ax[0].axvline(mean - (2* std), color='lime', linestyle='dashed', linewidth=0.75)

    ax[0].axvline(mean + (3* std), color='aquamarine', linestyle='dashed', linewidth=0.5, label='3 Std Dev')
    ax[0].axvline(mean - (3* std), color='aquamarine', linestyle='dashed', linewidth=0.5)

    ax[0].set_title(f'Histogram of {cname}')
    ax[0].set_xlabel(cname)
    ax[0].set_ylabel('Frequency')
    ax[0].legend()

    # Box Plot
    sns.boxplot(x=data, ax=ax[1])
    ax[1].set_title(f'Box Plot of {cname}')
    ax[1].set_xlabel(cname)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    print('This is a module for analyzing data. Please import it to use it.')