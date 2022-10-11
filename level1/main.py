import json
from datetime import datetime, timedelta


class Carrier:
    code: int
    delivery_promise: str

    def __init__(self, code, delivery_promise):
        self.code = code
        self.delivery_promise = delivery_promise


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
            carrier = Carrier(code=code, delivery_promise=delivery_promise)
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
                    expected_delivery_date = shipping_date + timedelta(days=carrier.delivery_promise + 1)
                    expected_delivery_str = expected_delivery_date.strftime("%Y-%m-%d")

            delivery = Delivery(package_id=package.package_id, expected_delivery=expected_delivery_str)
            self.deliveries.append(delivery)

            data["deliveries"].append({"package_id": delivery.package_id,
                                       "expected_delivery": delivery.expected_delivery})

        json_string = json.dumps(data)
        json_file = open("data/output.json", "w")
        json_file.write(json_string)
        json_file.close()


main = Main()
main.parse_input_file()
main.create_output_file()

