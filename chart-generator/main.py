from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def area_chart(ds, dateFmt):
    # create a subplot
    fig, ax = plt.subplots()

    # set figure size and dpi
    fig.set_size_inches(10, 5)
    fig.set_dpi(300)

    # draw the curves
    ax.fill_between(ds['Data'], ds['Casos acumulados'], color='#f44336',
                    label='Casos totais ({})'.format(ds['Casos acumulados'].values[-1]))
    ax.stackplot(ds['Data'], ds['Óbitos acumulados'], ds['Curados acumulados'], colors=['#9a9a9a', '#009688'], labels=[
                 'Óbitos totais ({})'.format(ds['Óbitos acumulados'].values[-1]), 'Curados totais ({})'.format(ds['Curados acumulados'].values[-1])])

    # write the total number at the end of the curves
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'),
            ds['Casos acumulados'].values[-1], str(ds['Casos acumulados'].values[-1]), color='w')
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'),
            ds['Curados acumulados'].values[-1], str(ds['Curados acumulados'].values[-1]), color='w')
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'),
            ds['Óbitos acumulados'].values[-1], str(ds['Óbitos acumulados'].values[-1]), color='w')

    # set chart style
    ax.xaxis.set_major_formatter(dateFmt)
    ax.grid(True)
    ax.set_facecolor('#101010')

    # set chart title
    ax.title.set_text('Situação geral da COVID-19 em Fernandópolis - {}'.format(
        ds['Data'].iloc[-1].strftime('%d/%m/%Y')))

    # draw legend on the upper left corner
    ax.legend(loc='upper left')

    # save chart as a png
    fig.savefig('../images/area_chart.png')


def bar_chart(ds, dateFmt):
    # create a subplot
    fig, ax = plt.subplots()

    # set figure size and dpi
    fig.set_size_inches(10, 5)
    fig.set_dpi(300)

    # draw the bars
    ax.bar(ds['Data'], ds['Novos casos'], color='#f44336', label='Casos novos de {} ({})'.format(
        ds['Data'].iloc[-1].strftime('%d/%m/%Y'), ds['Novos casos'].values[-1]))

    # write the number of cases at the top of each bar
    for date in ds['Data']:
        i = (date - datetime.fromisoformat('2020-03-25')).days
        y = ds['Novos casos'].values[i]
        if y != 0:
            ax.text(date - np.timedelta64(12, 'h'),
                    y + 0.25, str(y), color='w')

    # set chart style
    ax.xaxis.set_major_formatter(dateFmt)
    ax.grid(True)
    ax.set_facecolor('#101010')

    # set chart title
    ax.title.set_text('Casos novos da COVID-19 em Fernandópolis - {}'.format(
        ds['Data'].iloc[-1].strftime('%d/%m/%Y')))

    # draw legend on the upper left corner
    ax.legend(loc='upper left')

    # save chart as a png
    fig.savefig('../images/bar_chart.png')


def main():
    ds = pd.read_csv('../boletim-epidemiologico.csv')
    ds['Data'] = ds['Data'].map(
        lambda x: datetime.strptime(str(x), '%d/%m/%y'))
    dateFmt = mdates.DateFormatter('%d/%m')
    area_chart(ds, dateFmt)
    bar_chart(ds, dateFmt)


if __name__ == '__main__':
    main()
