# ds4a-grupo21
Group 21 repository of Data Science for All

This repository has all the scripts used to gather and engineer data for the bus optmization project our group is
conducting in DS4A course. Moreover, here we have a EDA of the SPTrans API data.

The final project is in the app directory. It is a dashboard that informs the historical time average between two bus 
stops. This data was gathered during 3 weeks using the get_bus_positions_to_sql.py and .sh scripts in an EC2 instance.

## Bus positions

We have a module to gather real-time bus position of São Paulo buses through. Here is how you can also gather the bus positions.

### How to?

In order to gather the bus positions data, you must have a "database" directory. Run the script get_bus_position_to_sql
to start tracking the positions. The script that gathers the data will automatically create a bus.db file to
store all the data gathered. 

## Passengers

We have a few modules to gather data about the number of passengers in each bus line daily. Here is how you can also
gather the bus positions.

### How to?

In order to gather the passengers data as in the Kaggle directory, there is a long way to go.

- Open passengers_download.py
- Set the *download_more_data* variable to True
- Add the years 2020 to 2013 in the years_to_scrap list. The values must be strings.
- Wait for all the data to be downloaded. If there is any bug, please let us know!
- There will be a lot of broken files. If you want to convert these files, you can use a online converter. However, if
you would not like to pay for this service, we recommend opening the files with Google Sheets and downloading them as
CSVs
- After converting all the files, run the passengers_formatter.py. This will format all the data and return a reasonably
clean data set of daily passengers data.

Wow! Huge amount of work! Now you can use whatever columns you want! For our Kaggle dataset we only used the total
amount of passengers.

## GTFS

The General Transit Feed Specification has overview data about São Paulo's bus system. You can find information such as
São Paulo's bus routes, bus stops, bus frequencies, stop times, and route shapes. We don't need to scrap this data since
it is available in SP Trans Developer website (http://www.sptrans.com.br/desenvolvedores/). However, we can store
everything as SQL.

### How to?

In order to transfer all the data to a unified SQL .db file, you need to:

- Create the "data" directory where the .git file is located.
- Create the "prod" directory inside "data."
- Insert the CSV files from the GTFS in the prod directory. (The files must be directly in the prod directory.)
- Run the create_sql_tables.py script. The script may try to convert CSVs that are not in the directory. If this happens,
you can comment the line and remove it from the "parameters" list.

The script will generate a bus.db file in the database directory. You must have this directory.
