import json
from datetime import datetime, timedelta


class Carrier:
    code: int
    delivery_promise: str
    saturday_deliveries: bool
    oversea_delay_threshold: int

    def __init__(self, code, delivery_promise, saturday_deliveries, oversea_delay_threshold):
        self.code = code
        self.delivery_promise = delivery_promise
        self.saturday_deliveries = saturday_deliveries
        self.oversea_delay_threshold = oversea_delay_threshold


class Package:
    package_id: int
    carrier: str
    shipping_date: str
    origin_country: str
    destination_country: str

    def __init__(self, package_id, carrier, shipping_date, origin_country, destination_country):
        self.package_id = package_id
        self.carrier = carrier
        self.shipping_date = shipping_date
        self.origin_country = origin_country
        self.destination_country = destination_country


class Delivery:
    package_id: int
    expected_delivery: str
    oversea_delay: bool

    def __init__(self, package_id, expected_delivery, oversea_delay):
        self.package_id = package_id
        self.expected_delivery = expected_delivery
        self.oversea_delay = oversea_delay


class Main:
    carriers: list
    packages: list
    deliveries: list

    def __init__(self):
        self.carriers = []
        self.packages = []
        self.deliveries = []

    def parse_input_file(self):
        # Opening JSON file
        file = open('data/input.json')
        data = json.load(file)

        # Carriers
        for carrier_data in data['carriers']:
            code = carrier_data["code"]
            delivery_promise = carrier_data["delivery_promise"]
            saturday_deliveries = carrier_data["saturday_deliveries"]
            oversea_delay_threshold = carrier_data["oversea_delay_threshold"]
            carrier = Carrier(code=code,
                              delivery_promise=delivery_promise,
                              saturday_deliveries=saturday_deliveries,
                              oversea_delay_threshold=oversea_delay_threshold)
            self.carriers.append(carrier)

        # Packages
        for package_data in data['packages']:
            package_id = package_data["id"]
            carrier = package_data["carrier"]
            shipping_date = package_data["shipping_date"]
            origin_country = package_data["origin_country"]
            destination_country = package_data["destination_country"]

            package = Package(package_id=package_id,
                              carrier=carrier,
                              shipping_date=shipping_date,
                              origin_country=origin_country,
                              destination_country=destination_country)
            self.packages.append(package)

        # Closing input file
        file.close()

    def create_output_file(self):
        data = {"deliveries": []}

        for package in self.packages:
            expected_delivery_str = ""

            for carrier in self.carriers:
                if package.carrier == carrier.code:
                    # todo Calculated delivery date is wrong!
                    expected_delivery_str = self.calculate_delivery_date(package, carrier.delivery_promise)

            data["deliveries"].append({"package_id": package.package_id,
                                      "expected_delivery": expected_delivery_str})

        json_string = json.dumps(data)
        json_file = open("data/output.json", "w")
        json_file.write(json_string)
        json_file.close()


    def calculate_delivery_date(self, package, delivery_promise: int) -> str:
        # todo Calculated delivery date is wrong!
        shipping_date = datetime.strptime(package.shipping_date, "%Y-%m-%d")
        expected_delivery_date = shipping_date + timedelta(days=delivery_promise + 1)
        is_saturday = expected_delivery_date.strftime('%w') == 5

        # You can print this, to see the name of the day
        # print(f"Week day: {expected_delivery_date.strftime('%A')}")

        if is_saturday:
            # todo This is wrong
            expected_delivery_date = expected_delivery_date + timedelta(days=1)

        if delivery_promise < self.calculate_country_distance(package):
            # Add one day (well..this is probably wrong)
            expected_delivery_date = expected_delivery_date + timedelta(days=1)

        expected_delivery_str = expected_delivery_date.strftime("%Y-%m-%d")
        return expected_delivery_str

    @staticmethod
    def calculate_country_distance(package) -> int:
        # todo
        return 0

main = Main()
main.parse_input_file()
main.create_output_file()
