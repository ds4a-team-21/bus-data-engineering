# This script webscrapps all Town Hall data about the daily bus usage in São Paulo.

from passengers_getter.scrapp_passenger_qnt import ScrappPassengerQnt
import os

# You can download more data and process everything, or only process what you have.
download_more_data = True
years_to_scrap = ['2019', '2018', '2017', '2016', '2015', '2014', '2013']

# Instatiates class
scrap = ScrappPassengerQnt(years_to_scrap)

# All the years URLs.
url_2020 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/agenda/index.php?p=292723'
url_2019 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=269652'
url_2018 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=247850'
url_2017 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=228269'
url_2016 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=209427'
url_2015 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=188767'
url_2014 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=152417'
url_2013 = 'https://www.prefeitura.sp.gov.br/cidade/secretarias/transportes/institucional/sptrans/' \
           'acesso_a_informacao/index.php?p=164379'

# Dictionary with year string and year URL.
url_list = {'2020': url_2020, '2019': url_2019, '2018': url_2018, '2017': url_2017,
            '2016': url_2016, '2015': url_2015, '2014': url_2014, '2013': url_2013}

# Gets only valid URLs. The valid URLs have their year in the year list.
valid_url_dict = {valid_url[0]: valid_url[1] for valid_url in url_list.items()
                  if valid_url[0] in years_to_scrap}

# Makes raw data directories.
scrap.mk_raw_data_dirs()

# Sets de base directory.
base_dir = os.path.abspath('data/raw/passengers')

# Variable explanation in line 7
if download_more_data:

    # For each year, download data.
    for year, url in valid_url_dict.items():
        year_dir = os.path.join(base_dir, year)
        scrap.download_qnt_passengers_csvs(year_dir, url)
