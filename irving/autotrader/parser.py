import re

from bs4 import BeautifulSoup

from irving.core.models import VehicleCondition
from irving.autotrader.models import AutotraderVehicleListing

_listing_id_re = re.compile(r"listingId=(\d*)")
_listing_id_tag_re = re.compile(r"vehicledetails")
_listing_title_re = re.compile(r"(Used|New) (\d{4}) (.*) (.*) (.*)")
_listing_owner_re = re.compile(r"(.*) \(([\d.]*) mi. away\)")


def parse_listings(path):
    listings = []
    with open(file=path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, features="html.parser")
    listing_tags = soup.find_all(class_="inventory-listing")
    for listing_tag in listing_tags:
        listing = parse_listing(listing_tag)
        listings.append(listing)
    return listings


def parse_listing(listing_tag):
    listing = AutotraderVehicleListing()
    listing.listing_id = parse_listing_id(listing_tag)
    try:
        condition, year, make, model, trim = parse_listing_title(listing_tag)
        listing.condition = condition.value
        listing.year = year
        listing.make = make
        listing.model = model
        listing.trim = trim
        listing.price = parse_listing_price(listing_tag)
        listing.miles = parse_listing_miles(listing_tag)
        listing.owner, listing.distance = parse_listing_owner(listing_tag)
        listing.listing_url = listing.format_listing_url(listing.listing_id)
        return listing
    except ValueError as exc:
        raise ValueError(
            f"Error parsing listing id {listing.listing_id}: {exc}"
        ) from exc


def parse_listing_id(listing_tag):
    listing_id_tag = listing_tag.find_next("a", attrs={"href": _listing_id_tag_re})
    if not listing_id_tag:
        raise ValueError("Listing ID tag not found.")
    listing_id_href = listing_id_tag.get("href")
    listing_id = _listing_id_re.search(listing_id_href).group(1)
    return listing_id


def parse_listing_title(listing_tag):
    title_tag = listing_tag.find_next("h2", attrs={"data-cmp": "subheading"})
    if not title_tag:
        raise ValueError("Listing title tag not found.")
    title_tag_text = title_tag.get_text()
    match = _listing_title_re.search(title_tag_text)
    if not match:
        raise ValueError("Listing title match not found.")
    if len(match.groups()) != 5:
        # pylint: disable-next=line-too-long
        raise ValueError(
            "Listing title match does not include condition, year, make, model, and trim."
        )
    condition = VehicleCondition(match.group(1).lower())
    year = int(match.group(2))
    make = match.group(3)
    model = match.group(4)
    trim = match.group(5)
    return condition, year, make, model, trim


def parse_listing_price(listing_tag):
    listing_price_tag = listing_tag.find_next(class_="first-price")
    if not listing_price_tag:
        return None
    listing_price = int(listing_price_tag.get_text().replace(",", ""))
    return listing_price


def parse_listing_miles(listing_tag):
    listing_miles_tag = listing_tag.find_next(
        "div", attrs={"class": "item-card-specifications"}
    ).find_next("div")
    if not listing_miles_tag:
        raise ValueError("Listing miles tag not found.")
    listing_miles_text = listing_miles_tag.get_text()
    if not listing_miles_text.endswith("miles"):
        return None
    listing_miles = int(listing_miles_text.replace(",", "").replace("miles", ""))
    return listing_miles


def parse_listing_owner(listing_tag):
    listing_owner_tag = listing_tag.find_next(
        "div", attrs={"data-cmp": "ownerDistance"}
    )
    if not listing_owner_tag:
        raise ValueError("Listing owner tag not found.")
    listing_owner_text = listing_owner_tag.get_text()
    listing_owner_matches = _listing_owner_re.search(listing_owner_text)
    if listing_owner_matches:
        listing_owner = listing_owner_matches.group(1)
        listing_distance = float(listing_owner_matches.group(2))
    else:
        listing_owner = listing_owner_text
        listing_distance = 0
    return listing_owner, listing_distance
