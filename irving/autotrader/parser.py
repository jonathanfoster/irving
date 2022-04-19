import csv
import re

from bs4 import BeautifulSoup

from irving.autotrader.models import AutotraderVehicleListing

listing_id_re = re.compile(r"listingId=(\d*)")
listing_id_tag_re = re.compile(r"vehicledetails")
owner_re = re.compile(r"(.*) \(([\d.]*) mi. away\)")


def parse_listings(path):
    listings = []
    with open(file=path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, features="html.parser")
    listing_tags = soup.find_all(class_="inventory-listing")
    for listing_tag in listing_tags:
        listing = parse_listing(listing_tag)
        # TODO: Check if listing is valid
        listings.append(listing)
    return listings


def parse_listing(listing_tag):
    # TODO: Parse year, make, model, and trim
    listing = AutotraderVehicleListing()
    listing.listing_id = parse_listing_id(listing_tag)
    listing.year = parse_listing_year(listing_tag)
    listing.make = parse_listing_make(listing_tag)
    listing.model = parse_listing_model(listing_tag)
    listing.trim = parse_listing_trim(listing_tag)
    listing.price = parse_listing_price(listing_tag)
    listing.miles = parse_listing_miles(listing_tag)
    listing.owner, listing.distance = parse_listing_owner(listing_tag)
    return listing


def parse_listing_id(listing_tag):
    listing_id_tag = listing_tag.find_next("a", attrs={"href": listing_id_tag_re})
    listing_id_href = listing_id_tag.get("href")
    listing_id = listing_id_re.search(listing_id_href).group(1)
    return listing_id


# TODO: Parse listing year
def parse_listing_year(listing_tag):
    return 2012


# TODO: Parse listing make
def parse_listing_make(listing_tag):
    return "Volkswagen"


# TODO: Parse listing model
def parse_listing_model(listing_tag):
    return "Jetta"


# TODO: Parse listing trim
def parse_listing_trim(listing_tag):
    return "SE"


def parse_listing_price(listing_tag):
    price_tag = listing_tag.find_next(class_="first-price")
    price = int(price_tag.get_text().replace(",", ""))
    return price


def parse_listing_miles(listing_tag):
    miles_tag = listing_tag.find_next(
        "div", attrs={"class": "item-card-specifications"}
    ).find_next("div")
    miles = int(miles_tag.get_text().replace(",", "").replace("miles", ""))
    return miles


def parse_listing_owner(listing_tag):
    owner_tag = listing_tag.find_next("div", attrs={"data-cmp": "ownerDistance"})
    owner_matches = owner_re.search(owner_tag.get_text())
    if owner_matches:
        owner = owner_matches.group(1)
        distance = float(owner_matches.group(2))
    else:
        owner = None
        distance = 0
    return owner, distance


def write_to_csv(path, listings):
    with open(file=path, mode="w", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        if len(listings) > 0:
            csv_writer.writerow(listings[0].__dict__.keys())
        for vehicle in listings:
            csv_writer.writerow(vehicle.__dict__.values())
