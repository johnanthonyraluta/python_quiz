import csv
import time
import json
import requests

from requests import Request, Session


class ValidateAddress:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.7,fr-BE;q=0.3",
            "Referer": "https://tools.usps.com/zip-code-lookup.htm?byaddress",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Connection": "keep-alive",
        }
        self.headers_sess = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0"
        }
        # self.usps_url = "https://tools.usps.com/zip-code-lookup.htm?byaddress"
        self.usps_url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"
        self.input_file = (
            "/home/jraluta/side_project/python_quiz/Python Quiz Input - Sheet1.csv"
        )
        self.output_file = (
            "/home/jraluta/side_project/python_quiz/Python Quiz Output - Sheet1.csv"
        )
        self.fields = ["Company", "Street", "City", "St", "ZIPCode", "Result"]

    def _read_input_per_line(self):
        self.data_list = []
        with open(self.input_file, newline="") as line_read:
            reader = csv.reader(line_read)
            for row_read in reader:
                if "Company" in row_read:
                    continue
                self.data_list.append(row_read)
        return self.data_list

    def _write_result(self, data_list_out):
        output = self.output_file
        with open(output, "w") as row_write:
            csvwriter = csv.writer(row_write)
            csvwriter.writerow(self.fields)
            csvwriter.writerows(data_list_out)

    def _check_address(self, tCompany, tAddress, tCity, tState, tZip_byaddress):
        session = requests.Session()
        payload = {
            "companyName": tCompany.strip(),
            "address1": tAddress.strip(),
            "city": tCity.strip(),
            "state": tState.strip(),
            "zip": tZip_byaddress.strip(),
            "encode": "form",
        }
        # validate_sess = session.get(
        #     url="https://tools.usps.com/zip-code-lookup.htm", headers=self.headers_sess
        # )
        # time.sleep(5)
        validate = session.post(
            self.usps_url,
            data=payload,
            headers=self.headers,
        )
        time.sleep(3)
        result = json.loads(validate.text)
        if result["resultStatus"] == "SUCCESS":
            return "Address Valid"
        elif result["resultStatus"] == "ADDRESS NOT FOUND":
            return "Address Invalid"


def execute_address_validation():
    print("Start Validating Address")
    validate_address = ValidateAddress()
    data_list_out = []
    data_list_in = validate_address._read_input_per_line()
    for data in data_list_in:
        print("Validating Address " + data[0])
        temp_list = []
        tCompany = data[0]
        temp_list.append(tCompany)
        tAddress = data[1]
        temp_list.append(tAddress)
        tCity = data[2]
        temp_list.append(tCity)
        tState = data[3]
        temp_list.append(tState)
        tZip_byaddress = data[4]
        temp_list.append(tZip_byaddress)
        address_result = validate_address._check_address(
            tCompany, tAddress, tCity, tState, tZip_byaddress
        )
        temp_list.append(address_result)
        data_list_out.append(temp_list)
        print(f"Address {data[0]} Validated Result: {address_result}")
    print("Validation done..writing data")
    validate_address._write_result(data_list_out)
    print("Data saved.")


if __name__ == "__main__":
    execute_address_validation()
