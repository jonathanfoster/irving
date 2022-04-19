from irving.core.models import VehicleListing


class AutotraderVehicleListing(VehicleListing):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.listing_id:
            self.listing_url = self.format_listing_url(self.listing_id)
        self.listing_source = "autotrader"

    @classmethod
    def format_listing_url(cls, listing_id):
        # pylint: disable-next=line-too-long
        return f"https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId={listing_id}"
