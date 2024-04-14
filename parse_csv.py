import csv
import re
import pandas as pd

def clean_text(text):
    """Clean the text by removing unwanted characters, spacing, speaker/date info, and URLs."""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Removing URLs
    text = re.sub(r'_Speaker_:\s*[^_]+_Date_:\s*[^_]+\n?', '', text)  # Removing speaker and date details
    text = re.sub(r'\\|"|,', '', text.strip())  # Remove backslashes, quotes, commas, and trim spaces
    return re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

def parse_glossary(file_path):
    """Read and parse the dogwhistle glossary to create a dataset."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            glossary_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

    entries = glossary_content.split('**')[1:]  # Split by bolded entry titles
    dataset = set()

    for i in range(0, len(entries), 2):
        term = entries[i].strip()
        details = entries[i + 1]

        surface_forms_match = re.search(r'_Surface forms_:\s*(.*?)\n', details)
        surface_forms = surface_forms_match.group(1).split('; ') if surface_forms_match else [term]

        covert_meaning_match = re.search(r'_Covert \(in-group\) meaning_:\s*(.*?)\n', details)
        covert_meaning = covert_meaning_match.group(1) if covert_meaning_match else "Unknown"

        example_context_match = re.search(r'Example context.*?\n\s*(.*?)(?=\n\S|\Z)', details, re.DOTALL)
        example_context = example_context_match.group(1).strip() if example_context_match else f"The term '{term}' is used in various contexts."

        for surface_form in surface_forms:
            input_text = clean_text(example_context.replace(term, surface_form))
            output_text = clean_text(covert_meaning)
            dataset.add((input_text, output_text))

    return list(dataset)  # Convert set to list for CSV writing

def write_to_csv(parsed_dataset, csv_file):
    """Write the parsed dataset to a CSV file."""
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['text', 'dogwhistle'])  # Header
            for input_text, _ in parsed_dataset:
                writer.writerow([input_text, 1])  # Assign '1' to each label
    except IOError:
        print(f"Error: Could not write to {csv_file}.")

# Running the parsing function on the glossary
file_path = 'dogwhistlegloss.md'
parsed_dataset = parse_glossary(file_path)

# Writing dataset to CSV
csv_file = 'dogwhistle_dataset.csv'
write_to_csv(parsed_dataset, csv_file)

if parsed_dataset:
    print(f"Dataset with {len(parsed_dataset)} unique entries has been saved to {csv_file}.")
