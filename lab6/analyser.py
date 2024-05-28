from dataloader.coinbaseloader import CoinbaseLoader, Granularity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def main():
    loader = CoinbaseLoader()
    currencies = ["APT-USD", "RAI-USD", "SNT-USD"]

    for currency in currencies:
        print(f"Аналіз валюти: {currency}\n")
        df_day = loader.get_historical_data(currency, "1 day", Granularity.ONE_MINUTE)
        df_month = loader.get_historical_data(currency, "30 days", Granularity.FIFTEEN_MINUTES)
        df_year = loader.get_historical_data(currency, "365 days", Granularity.ONE_HOUR)

        # Друкуємо кількість рядків для перевірки отриманих даних
        print(f"Дані за останній день:\n{df_day.head()}\n")
        print(f"Дані за останній місяць:\n{df_month.head()}\n")
        print(f"Дані за останній рік:\n{df_year.head()}\n")

        # Графіки (japanese candles) за останній день, місяць та рік
        fig, axs = plt.subplots(3, 1, figsize=(12, 10))
        fig.suptitle(f'Графіки котирувань для {currency}')
        axs[0].plot(df_day.index, df_day['close'], label='Ціна закриття', color='blue')
        axs[0].set_title('Останній день')
        axs[1].plot(df_month.index, df_month['close'], label='Ціна закриття', color='green')
        axs[1].set_title('Останній місяць')
        axs[2].plot(df_year.index, df_year['close'], label='Ціна закриття', color='orange')
        axs[2].set_title('Останній рік')

        for ax in axs:
            ax.grid(True)
            ax.legend()

        plt.show()

        # Базовий статистичний аналіз
        print("Статистичний аналіз:")
        for period, df in zip(["1 день", "1 місяць", "1 рік"], [df_day, df_month, df_year]):
            print(f"Дані за {period}:")
            print(f"Середнє значення ціни закриття: {df['close'].mean()}")
            print(f"Стандартне відхилення ціни закриття: {df['close'].std()}")
            rsa_10 = df['close'].rolling(window=10).mean().iloc[-1]
            rsa_20 = df['close'].rolling(window=20).mean().iloc[-1]
            rsa_50 = df['close'].rolling(window=50).mean().iloc[-1]
            print(f"RSA за 10 днів: {rsa_10}")
            print(f"RSA за 20 днів: {rsa_20}")
            print(f"RSA за 50 днів: {rsa_50}\n")

            # Графіки RSA
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df.index, df['close'], label='Ціна закриття', color='blue')
            ax.plot(df.index, df['close'].rolling(window=10).mean(), label='SMA 10 днів', color='green')
            ax.plot(df.index, df['close'].rolling(window=20).mean(), label='SMA 20 днів', color='orange')
            ax.plot(df.index, df['close'].rolling(window=50).mean(), label='SMA 50 днів', color='red')
            ax.set_title(f'Графік котирувань та RSA за {period} для {currency}')
            ax.legend()
            ax.grid(True)
            plt.show()

if __name__ == "__main__":
    main()
