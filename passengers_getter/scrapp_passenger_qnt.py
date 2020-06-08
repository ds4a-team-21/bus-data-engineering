from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from passengers_getter.helper import process_route_id, process_route_name


class ScrappPassengerQnt:

    # Default years list
    years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013']

    # When joining years, there are a lot of different names for the column. This dict normalizes the names
    column_transform = {'passageiros pagtes em dinheiro': 'passageiros pagantes em dinheiro',
                        'passageiros comum e vt': 'passageiros pagantes bilhete único comum',
                        'passageiros pgts bu comum m': 'passageiros pagantes bilhete único comum mensal',
                        'passageiros pagtes estudante': 'passageiros pagantes bilhete único estudante',
                        'passageiros pgts bu est mensal': 'passageiros pagantes bilhete único estudante mensal',
                        'passageiros pagtes bu vt': 'passageiros pagantes bilhete único vale transporte',
                        'passageiros pgts bu vt mensal': 'passageiros pagantes bilhete único vale transporte mensal',
                        'passageiros pagtes int m/cptm': 'passageiros pagantes integrações metrô e cptm',
                        'passageiros pgts int m/cptm m': 'passageiros pagantes integrações metrô e cptm mensal',
                        'passageiros int ‘nibus->‘nibus': 'passageiros integrações ônibus -> ônibus',
                        'passageiros int ônibus->ônibus': 'passageiros integrações ônibus -> ônibus',
                        'passageiros com gratuidade est': 'passageiros com gratuidade estudante',
                        'tot passageiros transportados': 'total passageiros transportados'}

    def __init__(self, years_list=years):

        self.years_list = years_list

        # Define directories
        self.directory_path = os.path.abspath('../data/raw/passengers/')
        self.year_dir = None
        self.monthly_dir = None
        self.daily_dir = None

    def mk_raw_data_dirs(self):
        """Making directories for each year. Inside the year's directory, creates daily and monthly
        passengers directories"""

        if not os.path.exists(os.path.abspath(self.directory_path)):
            os.mkdir(os.path.abspath(self.directory_path))

        for year in self.years_list:

            year_dir = os.path.join(self.directory_path, year)
            if not os.path.exists(os.path.abspath(year_dir)):
                self.year_dir = os.path.abspath(year_dir)
                os.mkdir(self.year_dir)

                self.monthly_dir = os.path.join(self.year_dir, 'monthly_passengers')
                os.mkdir(self.monthly_dir)

                self.daily_dir = os.path.join(self.year_dir, 'daily_passengers')
                os.mkdir(self.daily_dir)

    @staticmethod
    def redirect_broken_file(a, directory, file_string, filename):
        """There are several .xls files that are broken. This method redirects them to a broken_files direcotory."""

        broken_files_dir_path = os.path.join(directory, 'broken_files')
        if not os.path.exists(broken_files_dir_path):
            os.mkdir(broken_files_dir_path)

        if 'Total' in a.text:

            filepath = os.path.join(broken_files_dir_path, filename)
            if not os.path.exists(filepath):

                with open(filepath, 'wb') as f:
                    f.write(file_string.content)

        else:
            filepath = os.path.join(broken_files_dir_path, filename)

            if not os.path.exists(filepath):
                with open(filepath, 'wb') as f:
                    f.write(file_string.content)

    def download_qnt_passengers_csvs(self, directory, passengers_url):
        """This method downloads all excel files from the URLs"""

        # Defining directories
        monthly = os.path.join(directory, 'monthly_passengers')
        daily = os.path.join(directory, 'daily_passengers')

        # Requesting URL and instatiating BS scrapper.
        passengers = requests.get(passengers_url)
        soup = BeautifulSoup(passengers.content, features='html.parser')

        passengers_td_list = soup.find_all('td')
        passengers_a = [td.find('a') for td in passengers_td_list if td.find('a') is not None]

        # Iterates over the list of all the links to download the files.
        for a in passengers_a:
            href = a.attrs['href']

            index = href.find('www', 0, len(href))
            href = 'http://' + href[index:]

            print(f'Working on {href}...')

            filename = str(a).split('>')
            filename = filename[0].split('/')[-1].replace('"', '')

            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            try:
                passengers_df = pd.read_excel(href)
                filename = filename.replace('.xls', '.csv')

                if 'Total' in a.text:

                    filepath = os.path.join(monthly, filename)
                    if not os.path.exists(filepath):
                        passengers_df.to_csv(filepath)
                else:
                    filepath = os.path.join(daily, filename)
                    if not os.path.exists(filepath):
                        passengers_df.to_csv(filepath)

            except:
                print('Pandas could not read file... downloading bytes and sending to seperate folder.')
                file = session.get(href)
                self.redirect_broken_file(a, directory, file, filename)
                continue

    def format_file_names(self):
        """Files came with an extra HTML attribute after .xls. This mehtod fix this."""

        # Iterates over the years
        years_dir_list = os.listdir(self.directory_path)
        for year_dir in years_dir_list:
            print('In years...')

            year_dir = os.path.join(self.directory_path, year_dir)
            monthly = os.path.join(year_dir, 'monthly_passengers')
            daily = os.path.join(year_dir, 'daily_passengers')

            # Accesses the month directory
            for month in os.listdir(monthly):
                print('In month...')

                if month.find('.csv') != -1:
                    month = os.path.join(monthly, month)
                    i = month.find('.csv') + 4
                    new_month = month[:i]

                    os.rename(month, new_month)

            # Accesses the daily directory
            for day in os.listdir(daily):
                print('In days...')

                if day.find('.csv') != -1:
                    day = os.path.join(daily, day)
                    i = day.find('.csv') + 4
                    new_day = day[:i]

                    os.rename(day, new_day)

    @staticmethod
    def format_csv(df, year):
        """This method gets all the different forms of csvs and normalizes a good part of it. It gets
        the name of the colums and erases the blank lines where the names were."""

        # From 2018, csvs have a different layout
        if int(year) >= 2018:

            try:
                if df['Unnamed: 0'].iloc[0] == 0:
                    df.drop('Unnamed: 0', axis=1, inplace=True)

            except:
                pass

            print(f'Columns len is {len(df.columns)}\n')

            if not df.columns[0] == 'Data':
                columns = df.iloc[1].to_list()

                new_columns = []
                for column in columns:

                    column = column.lower()
                    i = column.find('\n')
                    if i != -1:
                        new_columns.append(column[:i])
                    else:
                        new_columns.append(column)

                df.columns = new_columns
                df = df.loc[:, ~df.columns.duplicated()]
                df.drop([0, 1], inplace=True)

                df.reset_index(drop=True, inplace=True)

            else:

                new_columns = []
                for column in df.columns:

                    column = column.lower()
                    i = column.find('\n')
                    if i != -1:
                        new_columns.append(column[:i])
                    else:
                        new_columns.append(column)

                df.columns = new_columns
                df = df.loc[:, ~df.columns.duplicated()]


        # Before 2018
        else:

            df.drop('Unnamed: 0', axis=1, inplace=True)
            if 'Unnamed: 0.1' in df.columns:
                df.columns = df.iloc[0].to_list()
                df.columns = [column.lower() for column in df.columns]

                df.drop(0, inplace=True)

            else:
                new_columns = []
                for column in df.columns:

                    column = column.lower()
                    i = column.find('\n')
                    if i != -1:

                        new_columns.append(column[:i])
                    else:
                        new_columns.append(column)

                df.columns = new_columns

        new_columns = []
        for column in df.columns:
            if column in ScrappPassengerQnt.column_transform.keys():
                column = ScrappPassengerQnt.column_transform[column]

            new_columns.append(column)

        if new_columns:
            df.columns = new_columns

        return df

    def concatenate_year_csv(self):

        for year in self.years_list:

            print(f'Starting year {year}')

            year_dir = os.path.join(self.directory_path, str(year))
            daily_dir = os.path.join(year_dir, 'daily_passengers')
            daily_files = os.listdir(daily_dir)

            df_list = []
            for i, file in enumerate(daily_files):

                if not file == '.DS_Store':

                    print(f'Converting file {file}')
                    filepath = os.path.join(daily_dir, file)
                    try:
                        df = pd.read_csv(filepath)
                    except:
                        df = pd.read_csv(filepath, encoding='iso-8859-1')

                    formatted = self.format_csv(df, year)

                    df_list.append(formatted)

            print(len(df_list))
            yearly_passengers = pd.concat(df_list, ignore_index=True)

            prod_daily_passengers_dir = os.path.join(self.directory_path ,'daily_passengers')
            if not os.path.exists(prod_daily_passengers_dir):
                os.mkdir(prod_daily_passengers_dir)

            filename = os.path.join(prod_daily_passengers_dir, str(year))

            print(f'\n\nSaving file as {filename}\n\n')
            yearly_passengers.to_csv(filename + '.csv', index=False)

    @staticmethod
    def format_final_csv_date(final: 'Final df'):

        # Little transformations in column data in order to convert strings well to datetime
        final['data'] = final['data'].str.replace('.', '')
        final['data'] = final['data'].str.replace('jan', '01')
        final['data'] = final['data'].str.replace('fev', '02')
        final['data'] = final['data'].str.replace('mar', '03')
        final['data'] = final['data'].str.replace('abr', '04')
        final['data'] = final['data'].str.replace('mai', '05')
        final['data'] = final['data'].str.replace('jun', '06')
        final['data'] = final['data'].str.replace('jul', '07')
        final['data'] = final['data'].str.replace('ago', '08')
        final['data'] = final['data'].str.replace('set', '09')
        final['data'] = final['data'].str.replace('out', '10')
        final['data'] = final['data'].str.replace('out', '11')
        final['data'] = final['data'].str.replace('dez', '12')
        final['data'] = final['data'].str.replace('42065', '')

        final['data'] = pd.to_datetime(final['data']).dt.date

        return final['data']

    def final_csv(self):

        # Getting path to directory with passengers years
        path_to_passengers = os.path.abspath('../data/raw/passengers/daily_passengers')
        passenger_files = os.listdir(path_to_passengers)
        passenger_files.remove('.DS_Store')

        df_list = []

        for file in passenger_files:
            path = os.path.join(path_to_passengers, file)
            df = pd.read_csv(path)
            df_list.append(df)

        passengers = pd.concat(df_list)

        passengers['data'] = self.format_final_csv_date(passengers)

        passengers.dropna(subset=['data', 'linha'], inplace=True)
        passengers.reset_index(drop=True, inplace=True)

        passengers['routes'] = passengers['linha'].apply(process_route_id)
        passengers['name'] = passengers['linha'].apply(process_route_name)

        passengers = passengers[
            ['data', 'tipo', 'area', 'empresa', 'routes', 'name', 'total passageiros transportados']].copy()

        passengers = passengers.reset_index()
        passengers.columns = ['index', 'date', 'type', 'area', 'company', 'routes', 'name', 'passengers']
        passengers.to_csv('../data/prod/passengers.csv', index=False)
