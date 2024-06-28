import pdfplumber
import pandas as pd


def extract_table_from_page(pdf, page_number):
    page = pdf.pages[page_number - 1]
    table = page.extract_tables()
    return table


def reverse_text_in_cells(table):
    return [[cell[::-1] if cell is not None else cell for cell in row] for row in table]


pdf_path = "data4.pdf"
start_page = 169
end_page = 222
output_csv_path = "output.csv"

all_dataframes = []


with pdfplumber.open(pdf_path) as pdf:
    initial_table = extract_table_from_page(pdf, start_page)
    if initial_table:
        extracted_table = initial_table[0]

        # Reverse the order of rows
        extracted_table.reverse()

        # Reverse text in each cell
        corrected_table = reverse_text_in_cells(extracted_table)

        # Transpose the corrected table to fix rows and columns
        transposed_table = list(map(list, zip(*corrected_table)))

        initial_df = pd.DataFrame(transposed_table[1:], columns=transposed_table[0])
        all_dataframes.append(initial_df)

    for page_number in range(start_page + 1, end_page + 1):
        table = extract_table_from_page(pdf, page_number)
        if table:
            extracted_table = table[0]

            extracted_table.reverse()

            corrected_table = reverse_text_in_cells(extracted_table)

            transposed_table = list(map(list, zip(*corrected_table)))

            df = pd.DataFrame(transposed_table[1:], columns=transposed_table[0])

            # Merge with the previous DataFrame horizontally for every two pages after the initial two pages
            if (page_number - start_page - 1) % 2 == 0:
                initial_df = pd.concat([initial_df, df.iloc[:, 2:]], axis=1)

initial_df.to_csv(output_csv_path, index=False)

print(f"Tables extracted successfully from pages {start_page} to {end_page} and saved to {output_csv_path}.")