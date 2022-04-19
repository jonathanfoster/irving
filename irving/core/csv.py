import csv


def write_to_csv(path, listings):
    with open(file=path, mode="w", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        if len(listings) > 0:
            csv_writer.writerow(listings[0].__dict__.keys())
        for vehicle in listings:
            csv_writer.writerow(vehicle.__dict__.values())
