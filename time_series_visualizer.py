import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Register the converters for date-time handling in pandas
register_matplotlib_converters()

# Import data and parse the 'date' column as datetime
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data: Remove top 2.5% and bottom 2.5% of pageviews
df = df[(df['page_views'] >= df['page_views'].quantile(0.025)) & (df['page_views'] <= df['page_views'].quantile(0.975))]

def draw_line_plot():
    # Make a copy of the data for the line plot
    df_line = df.copy()

    # Create the line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_line.index, df_line['page_views'], color='r', linewidth=1)
    
    # Set title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return the figure
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Make a copy of the data for the bar plot
    df_bar = df.copy()

    # Extract year and month from the date index
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Calculate the average daily page views per month for each year
    df_bar_grouped = df_bar.groupby(['year', 'month'])['page_views'].mean().unstack()

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar_grouped.plot(kind='bar', ax=ax)

    # Set title and labels
    ax.set_title('Average Daily Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Save image and return the figure
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare the data for the box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]

    # Create the figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Year-wise Box Plot
    sns.boxplot(data=df_box, x='year', y='page_views', ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')

    # Month-wise Box Plot
    sns.boxplot(data=df_box, x='month', y='page_views', ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return the figure
    fig.savefig('box_plot.png')
    return fig
