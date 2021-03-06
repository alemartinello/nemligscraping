import seaborn as sns
sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
from cycler import cycler


def define_NB_colors():
    """
    Defines Nationalbankens' colors and update matplotlib to use those as
    default. Sets the colors as matplotlib defaults and returns a color list 
    """
    c = cycler(
        'color',
        [
            (0/255, 123/255, 209/255),
            (146/255, 34/255, 156/255),
            (196/255, 61/255, 33/255),
            (223/255, 147/255, 55/255),
            (176/255, 210/255, 71/255),
            (102/255, 102/255, 102/255)
        ])
    plt.rcParams["axes.prop_cycle"] = c

    colorlist = [i['color'] for i in c.__dict__['_left']]
    return colorlist

def plot_figure():
    nb_colors = define_NB_colors()
    
    df = pd.read_csv('nemlig_scraping.csv')
    df['number_waiting'] = df['number_waiting'] #.fillna(0)
    df.time = (pd.to_datetime(df['time']))

    _, ax = plt.subplots(1,1, figsize=(15,6))

    hours = mdates.HourLocator(interval = 4)
    hours_all = mdates.HourLocator(interval = 1)
    fmt = mdates.DateFormatter('%d/%m %H:%M')

    ax = sns.lineplot(x="time", y="number_waiting", data=df, ax = ax)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_locator(hours_all)

    ax.set_ylabel("Online kø på nemlig.com")
    ax.set_xlabel("")

    plt.axvspan(pd.to_datetime('2020-03-13 19:00:00'), pd.to_datetime('2020-03-13 19:38:00'), color=nb_colors[1], alpha=0.5, lw=0)
    plt.annotate('  Pressemøde i\n  Statsministeriet\n  (grænselukning)', (pd.to_datetime('2020-03-13 19:40:00'), 15000), ha = 'left', color=nb_colors[1])

    plt.axvspan(pd.to_datetime('2020-03-17 13:30:00'), pd.to_datetime('2020-03-17 13:35:00'), color=nb_colors[1], alpha=0.5, lw=0)
    plt.annotate('Dronningens tale  \nbekendtgjorde  ', (pd.to_datetime('2020-03-17 13:35:00'), 15000), ha = 'right', color=nb_colors[1])

    plt.axvspan(pd.to_datetime('2020-03-17 19:00:00'), pd.to_datetime('2020-03-17 19:30:00'), color=nb_colors[1], alpha=0.5, lw=0)
    plt.annotate('Pressemøde i  \nStatsministeriet  \n ("køb online hvis i kan")', (pd.to_datetime('2020-03-17 19:00:00'), 45000), ha = 'right', color=nb_colors[1])

    plt.axvspan(pd.to_datetime('2020-03-17 20:00:00'), pd.to_datetime('2020-03-17 20:10:00'), color=nb_colors[1], alpha=0.5, lw=0)
    plt.annotate('  Dronningens tale', (pd.to_datetime('2020-03-17 20:00:00'), 5000), ha = 'left', color=nb_colors[1])

    plt.gcf().autofmt_xdate()

    plt.savefig('plot.pdf')
    return

