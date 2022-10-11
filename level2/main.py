import json
from datetime import datetime, timedelta


class Carrier:
    code: int
    delivery_promise: str
    saturday_deliveries: bool

    def __init__(self, code, delivery_promise, saturday_deliveries):
        self.code = code
        self.delivery_promise = delivery_promise
        self.saturday_deliveries = saturday_deliveries


class Package:
    package_id: int
    carrier: str
    shipping_date: str

    def __init__(self, package_id, carrier, shipping_date):
        self.package_id = package_id
        self.carrier = carrier
        self.shipping_date = shipping_date


class Delivery:
    package_id: int
    expected_delivery: str

    def __init__(self, package_id, expected_delivery):
        self.package_id = package_id
        self.expected_delivery = expected_delivery


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
            carrier = Carrier(code=code, delivery_promise=delivery_promise, saturday_deliveries=saturday_deliveries)
            self.carriers.append(carrier)

        # Packages
        for package_data in data['packages']:
            package_id = package_data["id"]
            carrier = package_data["carrier"]
            shipping_date = package_data["shipping_date"]
            package = Package(package_id=package_id, carrier=carrier, shipping_date=shipping_date)
            self.packages.append(package)

        # Closing input file
        file.close()

    def create_output_file(self):
        data = {"deliveries": []}

        for package in self.packages:
            shipping_date = datetime.strptime(package.shipping_date, "%Y-%m-%d")

            expected_delivery_str = ""

            for carrier in self.carriers:
                if package.carrier == carrier.code:
                    # todo Calculated delivery date is wrong!
                    expected_delivery_str = self.calculate_delivery_date(shipping_date, carrier.delivery_promise)

            delivery = Delivery(package_id=package.package_id, expected_delivery=expected_delivery_str)
            self.deliveries.append(delivery)

            data["deliveries"].append({"package_id": delivery.package_id,
                                       "expected_delivery": delivery.expected_delivery})

        json_string = json.dumps(data)
        json_file = open("data/output.json", "w")
        json_file.write(json_string)
        json_file.close()

    @staticmethod
    def calculate_delivery_date(shipping_date, delivery_promise: int) -> str:
        # todo Calculated delivery date is wrong!
        expected_delivery_date = shipping_date + timedelta(days=delivery_promise + 1)
        is_saturday = expected_delivery_date.strftime('%w') == 5

        # You can print this, to see the name of the day
        # print(f"Week day: {expected_delivery_date.strftime('%A')}")

        if is_saturday:
            expected_delivery_date = expected_delivery_date + timedelta(days=1)

        expected_delivery_str = expected_delivery_date.strftime("%Y-%m-%d")
        return expected_delivery_str


main = Main()
main.parse_input_file()
main.create_output_file()
