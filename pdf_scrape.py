import pdfplumber
import re


class PdfScraper:
    def __init__(self, filepath_1, filepath_2):
        super().__init__()

        self.filepath_1 = filepath_1
        self.filepath_2 = filepath_2

        self.index_criteria = ["29", "30"]

        # Get order numbers from pdf 1
        self.sage_report_order_numbers = self.scrape_pdf(
            filepath_1, self.index_criteria
        )
        # Get full lines of text from pdf 1
        self.sage_report_lines = self.extract_date_lines(filepath_1)

        # Get order numbers from pdf 2
        self.schedule_report = self.scrape_pdf(filepath_2, self.index_criteria)

    def scrape_pdf(self, filepath, index_criteria):

        order_number_pattern = r"\b\d{5,5}\b"

        with pdfplumber.open(filepath) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text()

        order_numbers = re.findall(order_number_pattern, all_text)

        index_criteria = index_criteria

        filtered_order_numbers = [
            order for order in order_numbers if order[:2] in index_criteria
        ]

        return filtered_order_numbers

    def extract_date_lines(self, filepath):
        date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}")
        matching_lines = []

        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                lines = page.extract_text().split("\n")
                for line in lines:
                    if date_pattern.match(line):
                        matching_lines.append(line)

        return matching_lines

    def parse_list_of_strs(self, str_input):
        str_input = str_input.split()

        due_date = str_input[0]
        name = " ".join(str_input[1:-4])
        order = str_input[-4]
        pm = str_input[-2]
        value = "£" + str_input[-1].replace(",", "")

        return {
            "name": name,
            "order": order,
            "due_date": due_date,
            "value": value,
            "pm": pm,
        }

    def out_put_text(self):
        missing_orders_numbers = []
        # Loop through pdf1 and pdf2 and append missing orders to list
        for sage_order in self.sage_report_order_numbers:
            if sage_order not in self.schedule_report:
                missing_orders_numbers.append(sage_order)

        missing_order_lines = []
        # loop through lines and check is order is present in line
        # then append line to list
        for line in self.sage_report_lines:
            for order in missing_orders_numbers:
                if order in line:
                    missing_order_lines.append(line)

        # loop through missing orders and create a list of dicts
        missing_orders = [
            self.parse_list_of_strs(entry) for entry in missing_order_lines
        ]

        output_string = "name, order, due_date, value, pm\n"
        for order_info in missing_orders:
            name = order_info["name"]
            order = order_info["order"]
            due_date = order_info["due_date"]
            value = order_info["value"]
            pm = order_info["pm"]

            output_string += f"{name}, {order}, {due_date}, {value}, {pm}\n"

        return output_string
