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


index_criteria = ["29", "30"]

sage_report = scrape_pdf("sales_orders.pdf", index_criteria)

schedule_report = scrape_pdf("scheduled_orders.pdf", index_criteria)

missing_orders = []

for sage_order in sage_report:
    if sage_order not in schedule_report:
        missing_orders.append(sage_order)

separator = "\n"
prefix = "\t-"
modified_list = [prefix + num for num in missing_orders]

my_str = separator.join(modified_list)

with open("text.txt", "w") as file:
    file.write("Missing packs:\n")
    file.write(my_str)
    file.close()
