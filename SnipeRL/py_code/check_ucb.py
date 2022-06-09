# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:22:01 2021

@author: Akileshvar A Mosi
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:11:01 2021

@author: Akileshvar A Mosi
"""


import math
import json
import random
from os import walk
import numpy as np
import pandas as pd
import quantstats as qs
from dateutil import parser
from tqdm import tqdm


class MultiArmBandit:

    __data = np.array
    __data_filepath = "data/15mins_data/"
    __amount_invested = 100000
    __magic_number = 4852
    __stock_dict = dict()

    def __init__(self):
        """
        Class Constructor

        Returns
        -------
        None.

        """
        pass

    def __update_average(self, old_avg, count, new_reward):
        """


        Parameters
        ----------
        old_avg : TYPE
            DESCRIPTION.
        count : TYPE
            DESCRIPTION.
        new_reward : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return ((old_avg * (count - 1)) + new_reward) / count

    def __update_confidence(self, average, count, pull_count):
        """


        Parameters
        ----------
        average : TYPE
            DESCRIPTION.
        count : TYPE
            DESCRIPTION.
        pull_count : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if count == 0:
            return 0
        return average + np.sqrt((2 * math.log(pull_count)) / count)

    def get_filepath(self):
        """
        This function returns the Filepath that is set, where the Stockwise
        data are available.

        Returns
        -------
        String


        """
        return self.__data_filepath

    def set_filepath(self, filepath):
        """
        This function is used to set the Filepath, where the Stockwise data
        are available.

        Parameters
        ----------
        filepath : String


        Returns
        -------
        None.

        """
        self.__data_filepath = filepath

    def get_data(self):
        """
        This function returns the array of data, which is used for the model.

        Returns
        -------
        np.array


        """
        return self.__data

    def set_data(self, path):
        """
        This function is used to set the data, which is used for the model, if
        we give the csv filepath of the data.

        Parameters
        ----------
        path : String


        Returns
        -------
        None.

        """
        self.__data = np.array(pd.read_csv(path))

    def get_stock_dict(self):
        """
        This function is used to get the dictionary which contains the Scrip
        Name equivalent to the numeric value, which was used in the model.

        Returns
        -------
        Dict


        """
        return self.__stock_dict

    def prepare_data(
        self,
        view="long",
        save_filename="",
        save_filepath="",
        shuffle_filename=False,
        file_order=None,
    ):
        """
        This data is used to prepare the dataset for the model.

        Parameters
        ----------
        save_filename : String, optional
            A filename is given if the dataset is needed to stored as a csv
            file. By default the dataset is not stored. The default is "".
        save_filepath : String, optional
            Path, where the dataset to be stored. The default is "".

        Returns
        -------
        None.

        """

        df_list = list()
        reward = list()
        last_close = list()
        if file_order is None:
            _, _, filenames = next(walk(self.__data_filepath))
        else:
            filenames = file_order

        if shuffle_filename:
            random.shuffle(filenames)

        for i in filenames:
            df_list.append(pd.read_csv(self.__data_filepath + i))

        self.__stock_dict = dict(zip(range(10), [i[:-4] for i in filenames]))
        for i in range(len(filenames)):
            reward.append(list())

        if view == "long":
            for i in range(len(df_list)):
                for j in range(1, len(df_list[i])):
                    prev = df_list[i]["Close"][j - 1]
                    curr = df_list[i]["Close"][j]
                    perc = ((curr - prev) / prev) * 100
                    reward[i].append(perc)
                last_close.append(curr)

        elif view == "short":
            for i in range(len(df_list)):
                for j in range(1, len(df_list[i])):
                    prev = df_list[i]["Close"][j - 1]
                    curr = df_list[i]["Close"][j]
                    perc = ((prev - curr) / prev) * 100
                    reward[i].append(perc)

        self.date_time = df_list[i]["Time"]
        rewardArray = (np.array(reward)).T
        rewardArray = rewardArray[~np.any(np.isnan(rewardArray), axis=1)]
        if save_filename != "":
            pd.DataFrame(rewardArray).to_csv(
                save_filepath + save_filename + ".csv", index=False
            )
        self.__data = rewardArray
        self.last_close = last_close

    def greedy_bandit(self, amount_invested=100000):
        """


        Parameters
        ----------
        amount_invested : TYPE, optional
            DESCRIPTION. The default is 100000.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return_amount = list()
        selected_scrip = list()
        capital = amount_invested
        avg_rew = [0] * self.__data.shape[1]
        count = [0] * self.__data.shape[1]
        for i in range(self.__data.shape[0]):
            if i < self.__data.shape[1]:
                arm = i
            else:
                arm = avg_rew.index(max(avg_rew))
            count[arm] += 1
            rew = self.__data[i, arm]
            amount_invested += (rew / 100) * amount_invested
            return_amount.append(amount_invested)
            selected_scrip.append(arm)
            avg_rew[arm] = self.__update_average(avg_rew[arm], count[arm], rew)
        return dict(
            average_reward=avg_rew,
            stock_count=count,
            return_amount=return_amount,
            selected_scrip=[self.__stock_dict[i] for i in selected_scrip],
            roi=((amount_invested - capital) / capital) * 100,
        )

    def epsilon_greedy(self, epsilon=0.02, amount_invested=100000):
        """


        Parameters
        ----------
        epsilon : TYPE
            DESCRIPTION.
        amount_invested : TYPE, optional
            DESCRIPTION. The default is 100000.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return_amount = list()
        selected_scrip = list()
        capital = amount_invested
        avg_rew = [0] * self.__data.shape[1]
        count = [0] * self.__data.shape[1]
        for i in range(self.__data.shape[0]):
            if i < self.__data.shape[1]:
                arm = i
            else:
                if (random.randint(0, 10000) * 0.0001) < epsilon:
                    arm = random.randint(0, self.__data.shape[1] - 1)
                else:
                    arm = avg_rew.index(max(avg_rew))
            count[arm] += 1
            rew = self.__data[i, arm]
            amount_invested += (rew / 100) * amount_invested
            return_amount.append(amount_invested)
            selected_scrip.append(arm)
            avg_rew[arm] = self.__update_average(avg_rew[arm], count[arm], rew)
        return dict(
            average_reward=avg_rew,
            stock_count=count,
            return_amount=return_amount,
            selected_scrip=[self.__stock_dict[i] for i in selected_scrip],
            roi=((amount_invested - capital) / capital) * 100,
        )

    def decay_epsilon_greedy(self, epsilon=0.02, amount_invested=100000):
        """


        Parameters
        ----------
        epsilon : TYPE
            DESCRIPTION.
        amount_invested : TYPE, optional
            DESCRIPTION. The default is 100000.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return_amount = list()
        selected_scrip = list()
        capital = amount_invested
        avg_rew = [0] * self.__data.shape[1]
        count = [0] * self.__data.shape[1]
        for i in range(self.__data.shape[0]):
            if i < self.__data.shape[1]:
                arm = i
            else:
                if (random.randint(0, 100) * 0.01) < epsilon:
                    arm = random.randint(0, self.__data.shape[1] - 1)
                else:
                    arm = avg_rew.index(max(avg_rew))
                epsilon *= 0.9
            count[arm] += 1
            selected_scrip.append(arm)
            rew = self.__data[i, arm]
            amount_invested += (rew / 100) * amount_invested
            return_amount.append(amount_invested)
            avg_rew[arm] = self.__update_average(avg_rew[arm], count[arm], rew)
        return dict(
            average_reward=avg_rew,
            stock_count=count,
            return_amount=return_amount,
            selected_scrip=[self.__stock_dict[i] for i in selected_scrip],
            roi=((amount_invested - capital) / capital) * 100,
        )

    def incremental_uniform(self, amount_invested=100000):
        """


        Parameters
        ----------
        amount_invested : TYPE, optional
            DESCRIPTION. The default is 100000.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        avg_rew = [0] * self.__data.shape[1]
        count = [0] * self.__data.shape[1]
        return_amount = list()
        selected_scrip = list()
        capital = amount_invested
        for i in range(self.__data.shape[0]):
            arm = i % self.__data.shape[1]
            count[arm] += 1
            selected_scrip.append(arm)
            rew = self.__data[i, arm]
            amount_invested += (rew / 100) * amount_invested
            return_amount.append(amount_invested)
            avg_rew[arm] = self.__update_average(avg_rew[arm], count[arm], rew)
        return dict(
            average_reward=avg_rew,
            stock_count=count,
            return_amount=return_amount,
            selected_scrip=[self.__stock_dict[i] for i in selected_scrip],
            roi=((amount_invested - capital) / capital) * 100,
        )

    def upper_confidence_bound(self, exploration=None, amount_invested=100000):
        """


        Parameters
        ----------
        exploration : int, optional
            DESCRIPTION. The default is None.
        amount_invested : float, optional
            DESCRIPTION. The default is 100000.

        Returns
        -------
        TYPE dict
            Returns a series of objects which includes

            method : string
                Name of the method with the exploration number.

            average_rew : list
                Average reward of all the stocks over the time.

            stock_count : list
                Number of times the algorithm picked that specific stock.

            return_amount : list
                Returns earned at each time step.

            selected_scrip : list
                List of scrip selected by the algorithm at specific time.

            roi : float64
                Return on Investment

            confidence : Array of float64
                Confidence of the algorithm on each stock at every iteration.

            iteration : int
                Total number of iterations.


        """

        if exploration == None:
            exploration = self.__magic_number
        return_amount = list()
        selected_scrip = list()
        confidence_list = list()
        capital = amount_invested
        avg_rew = [0] * self.__data.shape[1]
        count = [0] * self.__data.shape[1]
        confidence = [0] * self.__data.shape[1]
        for i in range(self.__data.shape[0]):
            if i < exploration:
                arm = i % self.__data.shape[1]
            else:
                arm = confidence.index(max(confidence))
            count[arm] += 1
            selected_scrip.append(arm)
            rew = self.__data[i, arm]
            amount_invested += (rew / 100) * amount_invested
            return_amount.append(amount_invested)
            avg_rew[arm] = self.__update_average(avg_rew[arm], count[arm], rew)
            for hand_ind in range(self.__data.shape[1]):
                confidence[hand_ind] = self.__update_confidence(
                    avg_rew[hand_ind], count[hand_ind], i + 1
                )
            confidence_list.extend(confidence)
        confidence_array = np.array(confidence_list).reshape(self.__data.shape)
        return dict(
            method="UCB" + str(exploration),
            average_reward=avg_rew,
            stock_count=count,
            return_amount=return_amount,
            selected_scrip=[self.__stock_dict[i] for i in selected_scrip],
            time=self.date_time[1:],
            roi=((amount_invested - capital) / capital) * 100,
            confidence=confidence_array.tolist(),
            iteration=i,
            stock_dict=self.__stock_dict,
        )

    def get_day_percent(self, data, slicer=25):
        """


        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        slicer : TYPE, optional
            DESCRIPTION. The default is 25.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        new_time = [
            (parser.parse(i).replace(tzinfo=None)) for i in tqdm(self.date_time)
        ]
        return_amount = data["return_amount"]
        day_time = [parser.parse((i.date()).ctime()) for i in new_time[::slicer]]
        day_return = return_amount[::slicer]
        return_series = pd.Series(day_return, index=day_time, name="return_series")
        return qs.utils.to_returns(return_series)

    def get_report(self, data, report_type, filename=""):
        """


        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        report_type : TYPE
            DESCRIPTION.
        filename : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """

        return_series = self.get_day_percent(data)
        if report_type == "html":
            qs.reports.html(return_series, output=filename, title=data["method"])
        elif report_type == "full":
            qs.reports.full(return_series)
        elif report_type == "basic":
            qs.reports.basic(return_series)

    def plot(self, data, plot_type=""):
        """


        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        plot_type : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        None.

        """
        return_series = self.get_day_percent(data)
        if plot_type == "daily_returns":
            qs.plots.daily_returns(return_series)
        elif plot_type == "distribution":
            qs.plots.distribution(return_series)
        elif plot_type == "drawdown":
            qs.plots.drawdown(return_series)
        elif plot_type == "drawdowns_periods":
            qs.plots.drawdowns_periods(return_series)
        elif plot_type == "earnings":
            qs.plots.earnings(return_series)
        elif plot_type == "histogram":
            qs.plots.histogram(return_series)
        elif plot_type == "log_returns":
            qs.plots.log_returns(return_series)
        elif plot_type == "monthly_returns":
            qs.plots.monthly_returns(return_series)
        elif plot_type == "monthly_heatmap":
            qs.plots.monthly_heatmap(return_series)
        elif plot_type == "plotly":
            qs.plots.plotly(return_series)
        elif plot_type == "returns":
            qs.plots.returns(return_series)
        elif plot_type == "rolling_beta":
            qs.plots.rolling_beta(return_series)
        elif plot_type == "rolling_sharpe":
            qs.plots.rolling_sharpe(return_series)
        elif plot_type == "rolling_sortino":
            qs.plots.rolling_sortino(return_series)
        elif plot_type == "rolling_volatility":
            qs.plots.rolling_volatility(return_series)
        elif plot_type == "snapshot":
            qs.plots.snapshot(return_series)
        elif plot_type == "to_plotly":
            qs.plots.to_plotly(return_series)
        elif plot_type == "warnings":
            qs.plots.warnings(return_series)
        elif plot_type == "yearly_returns":
            qs.plots.yearly_returns(return_series)

    def updater(self, final):
        with open("RLmethods/data/checkpoint.json") as file:
            checkpoint = json.load(file)

        last_close = checkpoint["last_close"]

        perc_change = list()
        for curr, prev in zip(final, last_close):
            perc_change.append(((curr - prev) / prev) * 100)

        confidence = checkpoint["confidence"]
        count = checkpoint["stock_count"]
        avg_rew = checkpoint["average_reward"]
        iteration = checkpoint["iteration"]

        arm = confidence.index(max(confidence))
        count[arm] += 1
        rew = perc_change[arm]
        avg_rew[arm] = self.__update_average(avg_rew[arm], count[arm], rew)
        for hand_ind in range(10):
            confidence[hand_ind] = self.__update_confidence(
                avg_rew[hand_ind], count[hand_ind], iteration + 1
            )
