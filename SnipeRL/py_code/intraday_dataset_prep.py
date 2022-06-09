import pandas as pd
import datetime as dt
import requests
from config import enctoken, kf_session, public_token, user_id, path_to_stocklist, path_to_store_data


class FetchData:
    
    def __init__(self, start, end, timeframe = 'day'):

        self.timeframe = timeframe
        self.fromdate = start
        self.todate = end
        self.stocks_to_fetch = pd.read_csv(path_to_stocklist)

    def connect(self, ID, current_date, next_date):

        url = "https://kite.zerodha.com/oms/instruments/historical/" + str(ID) + "/" + self.timeframe
        response = requests.get(
        url = url,
        params = {
            'user_id': user_id,
            'oi': "1",
            'from': current_date,
            'to': next_date,
            'kf_session': kf_session,
            'public_token': public_token,
            'user_id': user_id,
            'enctoken': enctoken
            },
            headers = {'authorization': enctoken},
            )
        #print(response.json())
        return response.json()['data']['candles']

    def get_data(self):

        for _ , row in self.stocks_to_fetch.iterrows():
            ID=row['Stock ID']
            stock_name=row['Stock']
        
            print('fetching ' + stock_name + '........')

            # Prepare time range to fetch data
            start_date = dt.datetime.strptime(self.fromdate, '%Y-%m-%d').date()
            end_date = dt.datetime.strptime(self.todate, '%Y-%m-%d').date()

            # Initialise Dataframe to collect stock data from start-end date
            stock_data = pd.DataFrame(columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Stock','Date'])

            # Begin iterating time range by multiple of 30 days
            current_date = start_date
            while current_date< end_date:
                next_date = current_date + dt.timedelta(days = 30)

                if next_date > dt.datetime.strptime(dt.datetime.today().strftime('%Y-%m-%d'),'%Y-%m-%d').date():
                    next_date = end_date
            
                current_date_range=current_date.strftime('%Y-%m-%d') +"&to=" + next_date.strftime('%Y-%m-%d')

                print('fetching' + current_date_range + '......')

                # fetch the data for the current iteration of date range

                data = self.connect(ID, current_date, next_date)

                if len(data) < 5:
                    current_date = current_date + dt.timedelta(days = 30)

                df = self.process_data(data, stock_name)
                stock_data = stock_data.append(df, ignore_index = True)
                print('Done!') 

                # increment current_date by 30 to fetch the next 30 days data
                current_date = current_date + dt.timedelta(days=30)

            # Once every date is covered loop exits and save the stock data before moving to next stock
            stock_data.to_csv(path_to_store_data + stock_name + '.csv', index = False)
            print(stock_name + 'Finished !')

        print('Success!')

    def process_data(self, data, stock_name):

        df = pd.DataFrame(data , columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Stock'])
        df.loc[df['Stock'] == df['Stock'][0], 'Stock'] = stock_name
        df["Date"] = ''
    
        for row in df['Time'].iteritems():
            df['Date'][row[0]] = row[1].split('T')[0]
            df['Time'][row[0]] = row[1].split('T')[1].split('+')[0]

        return df

#obj = FetchData('2021-02-01','2021-02-20')
#obj.get_data()