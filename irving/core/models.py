class VehicleListing:
    def __init__(self, **kwargs):
        self.listing_id = kwargs.get("listing_id", None)
        self.year = kwargs.get("year", None)
        self.make = kwargs.get("make", None)
        self.model = kwargs.get("model", None)
        self.trim = kwargs.get("trim", None)
        self.miles = kwargs.get("miles", 0)
        self.price = kwargs.get("price", 0)
        self.owner = kwargs.get("owner", None)
        self.distance = kwargs.get("distance", 0)
        self.listing_source = kwargs.get("listing_source", None)
        self.listing_url = kwargs.get("listing_url", None)
