from passengers_getter.scrapp_passenger_qnt import ScrappPassengerQnt

scrap = ScrappPassengerQnt()

# Format file names. Some of them did not have .xls or .csv as the final extension.
scrap.format_file_names()

# Generates yearly csvs from the daily observations of each bus line.
scrap.concatenate_year_csv()

# Generates a big csv with all the years.
scrap.final_csv()
