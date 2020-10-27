from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt


def area_chart(ds, dateFmt):
    # create a subplot
    fig, ax = plt.subplots()

    # set figure size and dpi
    fig.set_size_inches(10, 5)
    fig.set_dpi(300)

    # draw the curves
    ax.fill_between(
        ds['Data'],
        ds['Casos acumulados'],
        color='#f44336',
        label='Casos totais ({})'.format(ds['Casos acumulados'].values[-1]))
    ax.stackplot(
        ds['Data'],
        ds['Óbitos acumulados'],
        ds['Curados acumulados'],
        colors=['#9a9a9a', '#009688'],
        labels=[
            'Óbitos totais ({})'.format(ds['Óbitos acumulados'].values[-1]),
            'Curados totais ({})'.format(ds['Curados acumulados'].values[-1])])

    # write the total number at the end of the curves
    ax.text(
        ds['Data'].values[-1] + np.timedelta64(12, 'h'),
        ds['Casos acumulados'].values[-1],
        str(ds['Casos acumulados'].values[-1]),
        color='w')
    ax.text(
        ds['Data'].values[-1] + np.timedelta64(12, 'h'),
        ds['Curados acumulados'].values[-1],
        str(ds['Curados acumulados'].values[-1]),
        color='w')
    ax.text(
        ds['Data'].values[-1] + np.timedelta64(12, 'h'),
        ds['Óbitos acumulados'].values[-1],
        str(ds['Óbitos acumulados'].values[-1]),
        color='w')

    # set chart style
    ax.xaxis.set_major_formatter(dateFmt)
    ax.set_facecolor('#101010')

    # set chart title
    ax.title.set_text(
        'Situação geral da COVID-19 em Fernandópolis - {}'
            .format(ds['Data'].iloc[-1].strftime('%d/%m/%Y')))

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

    # calculate moving average
    moving_average = ds['Novos casos'].rolling(window=14).mean()

    # draw the bars
    ax.bar(
        ds['Data'],
        ds['Novos casos'],
        color='#f44336',
        label='Casos novos de {} ({})'.format(
            ds['Data'].iloc[-1].strftime('%d/%m/%Y'),
            ds['Novos casos'].values[-1]))
    ax.plot(
        ds['Data'],
        moving_average,
        color='#f4a235',
        linestyle='dashed',
        label='Média móvel de casos novos ({})'.format(
            int(np.trunc(moving_average.iloc[-1]))))

    # write the number of cases at the top of each bar
    for date in ds['Data']:
        i = (date - datetime.fromisoformat('2020-03-25')).days
        y = ds['Novos casos'].values[i]
        if y != 0:
            ax.text(
                date - np.timedelta64(12, 'h'),
                y + 0.25,
                str(y),
                color='w')

    # set chart style
    ax.xaxis.set_major_formatter(dateFmt)
    ax.set_facecolor('#101010')

    # set chart title
    ax.title.set_text(
        'Casos novos da COVID-19 em Fernandópolis - {}'
            .format(ds['Data'].iloc[-1].strftime('%d/%m/%Y')))

    # draw legend on the upper left corner
    ax.legend(loc='upper left')

    # save chart as a png
    fig.savefig('../images/bar_chart.png')


def line_chart(ds, dateFmt):
    # create a subplot
    fig, ax = plt.subplots()

    # set figure size and dpi
    fig.set_size_inches(10, 5)
    fig.set_dpi(300)

    # polynomial function
    def func(x, a, b, c, d, e, f, g):
        params = [a, b, c, d, e, f, g]
        n = len(params)
        total = 0
        for i in range(0, n):
            total += params[n - i - 1] * np.power(x, i)
        return total

    # optimized parameters for exponential curve fitting
    optimizedParameters, _ = opt.curve_fit(
        func,
        ds['Data'].map(
            lambda x: (x - datetime.fromisoformat('2020-03-25')).days),
        ds['Casos acumulados'])

    # list of days extended over 7 days
    extDate = ds['Data'].copy()
    for i in range(1, 8):
        extDate = extDate.append(
            pd.Series(
                [ds['Data'].iloc[-1] + timedelta(days=i)],
                index=[ds['Data'].size + i - 1]))

    # draw the curves
    ax.plot(
        ds['Data'],
        ds['Casos acumulados'],
        color='#f44336',
        label='Casos totais ({})'.format(ds['Casos acumulados'].values[-1]))
    ax.plot(
        extDate,
        func(
            extDate.map(
                lambda x: (x - datetime.fromisoformat('2020-03-25')).days),
            *optimizedParameters),
        color='#f4a235',
        linestyle='dashed',
        label='Projeção do número de casos até {} ({:.0f})'.format(
            extDate.iloc[-1].strftime('%d/%m/%Y'),
            np.floor(func(
                (extDate.iloc[-1] - datetime.fromisoformat('2020-03-25')).days,
                *optimizedParameters))))

    # write the number of cases at the end of the curve
    ax.text(
        ds['Data'].values[-1] + np.timedelta64(12, 'h'),
        ds['Casos acumulados'].values[-1],
        str(ds['Casos acumulados'].values[-1]),
        color='w')
    ax.text(
        extDate.iloc[-1] + timedelta(hours=12),
        func(
            (extDate.iloc[-1] - datetime.fromisoformat('2020-03-25')).days,
            *optimizedParameters),
        '{:.0f}'.format(
            np.floor(func(
                (extDate.iloc[-1] - datetime.fromisoformat('2020-03-25')).days,
                *optimizedParameters))),
        color='w')

    # set chart style
    ax.xaxis.set_major_formatter(dateFmt)
    ax.set_facecolor('#101010')

    # set chart title
    ax.title.set_text(
        'Casos da COVID-19 em Fernandópolis - {}'
            .format(ds['Data'].iloc[-1].strftime('%d/%m/%Y')))

    # draw legend on the upper left corner
    ax.legend(loc='upper left')

    # save chart as a png
    fig.savefig('../images/line_chart.png')


def main():
    ds = pd.read_csv('../boletim-epidemiologico.csv')
    ds['Data'] = ds['Data'].map(
        lambda x: datetime.strptime(str(x), '%d/%m/%y'))
    dateFmt = mdates.DateFormatter('%d/%m/%y')
    area_chart(ds, dateFmt)
    bar_chart(ds, dateFmt)
    line_chart(ds, dateFmt)


if __name__ == '__main__':
    main()
