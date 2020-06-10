from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def area_chart(ds, dateFmt):
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    fig.set_dpi(300)
    ax.fill_between(ds['Data'], ds['Casos acumulados'],
                    label='Casos totais ({})'.format(ds['Casos acumulados'].values[-1])).set_color('#f44336')
    sp = ax.stackplot(ds['Data'], ds['Óbitos acumulados'], ds['Curados acumulados'],
                      labels=['Óbitos totais ({})'.format(ds['Óbitos acumulados'].values[-1]), 'Curados totais ({})'.format(ds['Curados acumulados'].values[-1])])
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'),
            ds['Casos acumulados'].values[-1], str(ds['Casos acumulados'].values[-1]), color='w')
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'), ds['Curados acumulados'].values[-1],
            str(ds['Curados acumulados'].values[-1]), color='w')
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'), ds['Óbitos acumulados'].values[-1],
            str(ds['Óbitos acumulados'].values[-1]), color='w')
    sp[0].set_color('#9a9a9a')
    sp[1].set_color('#009688')
    ax.xaxis.set_major_formatter(dateFmt)
    ax.grid(True)
    ax.set_facecolor('#101010')
    ax.title.set_text(
        'Situação geral da COVID-19 em Fernandópolis - {}'.format(ds['Data'].iloc[-1].strftime('%d/%m/%Y')))
    ax.legend(loc='upper left')
    fig.savefig('../images/area_chart.png')


def line_chart(ds, dateFmt):
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    fig.set_dpi(300)
    ax.plot(ds['Data'], ds['Casos acumulados'], label='Casos totais ({})'.format(
        ds['Casos acumulados'].values[-1]))[0].set_color('#f44336')
    ax.plot(ds['Data'], np.poly1d(np.polyfit(ds['Data'], ds['Casos acumulados'], 1)),
            label='Linha de tendência')[0].set_color('#f44336')
    ax.text(ds['Data'].values[-1] + np.timedelta64(12, 'h'),
            ds['Casos acumulados'].values[-1], str(ds['Casos acumulados'].values[-1]), color='w')
    ax.xaxis.set_major_formatter(dateFmt)
    ax.set_facecolor('#101010')
    ax.title.set_text('Casos confirmados de COVID-19 em Fernandópolis - {}'.format(
        ds['Data'].iloc[-1].strftime('%d/%m/%Y')))
    ax.legend(loc='upper left')
    fig.savefig('../images/line_chart.png')


def main():
    ds = pd.read_csv('../boletim-epidemiologico.csv')
    ds['Data'] = ds['Data'].map(
        lambda x: datetime.strptime(str(x), '%d/%m/%y'))
    dateFmt = mdates.DateFormatter('%d/%m')
    area_chart(ds, dateFmt)
    # line_chart(ds, dateFmt)


if __name__ == '__main__':
    main()
