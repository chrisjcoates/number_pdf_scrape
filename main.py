import pdfplumber
import re


def scrape_pdf(filepath, index_criteria):

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


def extract_date_lines(filepath):
    date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}")
    matching_lines = []

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split("\n")
            for line in lines:
                if date_pattern.match(line):
                    matching_lines.append(line)

    return matching_lines


def parse_list_of_strs(str_input):
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


index_criteria = ["29", "30"]

# Get order numbers from pdf 1
sage_report_order_numbers = scrape_pdf("sales_orders.pdf", index_criteria)
# Get full lines of text from pdf
sage_report_lines = extract_date_lines("sales_orders.pdf")

# Get order numbers from pdf 2
schedule_report = scrape_pdf("scheduled_orders.pdf", index_criteria)


missing_orders_numbers = []
# Loop through pdf1 and pdf2 and append missing orders to list
for sage_order in sage_report_order_numbers:
    if sage_order not in schedule_report:
        missing_orders_numbers.append(sage_order)

missing_order_lines = []
# loop through lines and check is order is present in line
# then append line to list
for line in sage_report_lines:
    for order in missing_orders_numbers:
        if order in line:
            missing_order_lines.append(line)

# loop through missing orders and create a list of dicts
missing_orders = [parse_list_of_strs(entry) for entry in missing_order_lines]

with open("missing_orders.csv", "w") as file:
    file.write("name, order, due_date, value, pm\n")
    for order_info in missing_orders:
        name = order_info["name"]
        order = order_info["order"]
        due_date = order_info["due_date"]
        value = order_info["value"]
        pm = order_info["pm"]

        order_str = f"{name}, {order}, {due_date}, {value}, {pm}\n"
        file.write(order_str)
