import pdfplumber
import pandas as pd


# Function to extract tables from PDFs and handle disoriented tables
def extract_table_from_pdf(pdf_path, pages, year, correct_orientation=False):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in pages:
            print(f"Extracting from page: {page_num} of {pdf_path}")
            page = pdf.pages[page_num - 1]  # Correcting for zero-indexing
            table = page.extract_table()
            if table:
                if correct_orientation:
                    # Correct orientation
                    table.reverse()
                    table = [
                        [cell[::-1] if cell is not None else cell for cell in row]
                        for row in table
                    ]
                    table = list(map(list, zip(*table)))  # Transpose table
                tables.append(table)

    if not tables:
        print(f"No tables found in {pdf_path}")
        return pd.DataFrame()

    df_list = []
    first_table = tables[0]
    headers = first_table[0]  # Use the first row as the header
    print(f"Headers for {pdf_path}: {headers}")

    # Ensure each row has the correct number of columns
    df_first = pd.DataFrame(
        [row for row in first_table[2:] if len(row) == len(headers)], columns=headers
    )
    df_list.append(df_first)

    if len(tables) > 1:
        second_table = tables[1]
        df_second = pd.DataFrame(
            [row for row in second_table[3:] if len(row) == len(headers)],
            columns=headers,
        )
        df_list.append(df_second)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.insert(1, "Year", year)
    return combined_df


# PDF information with page numbers and whether orientation correction is needed
pdfs_info = [
    {
        "path": "Data/data3.pdf",
        "pages": [341, 342],
        "year": "2075/76",
        "output": "Output/output3_veg_76.csv",
        "correct_orientation": False,
    },
    {
        "path": "Data/data5.pdf",
        "pages": [208, 209],
        "year": "2077/78",
        "output": "Output/output5_veg_78.csv",
        "correct_orientation": False,
    },
    {
        "path": "Data/data4.pdf",
        "pages": [225, 226],
        "year": "2076/77",
        "output": "Output/output4_veg_77.csv",
        "correct_orientation": True,
    },
    {
        "path": "Data/data6.pdf",
        "pages": [194, 195],
        "year": "2078/79",
        "output": "Output/output6_veg_79.csv",
        "correct_orientation": True,
    },
]

for pdf_info in pdfs_info:
    data = extract_table_from_pdf(
        pdf_info["path"],
        pdf_info["pages"],
        pdf_info["year"],
        pdf_info["correct_orientation"],
    )
    data.to_csv(pdf_info["output"], index=False)
    print(f"Data has been successfully extracted and saved to {pdf_info['output']}.")
