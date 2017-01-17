import csv

CSV_DELIMETER = ','
CSV_QUOTECHAR = '"'


def write_csv_data(filename, data):
    if filename is not None:
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=CSV_DELIMETER, quotechar=CSV_QUOTECHAR, quoting=csv.QUOTE_ALL)
            csvwriter.writerow(data)
