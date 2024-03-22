import csv
import re

def clean_text(text):
    """Clean the text by removing unwanted characters, spacing, speaker/date info, and URLs."""
    # Removing URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Removing speaker and date details
    text = re.sub(r'_Speaker_:\s*[^_]+_Date_:\s*[^_]+\n?', '', text)
    # Trim white spaces
    text = text.strip()
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove backslashes and quotes
    text = re.sub(r'\\', '', text)
    text = re.sub(r'"', '', text)
    return text

def parse_glossary(file_path):
    """Read and parse the dogwhistle glossary to create a dataset."""
    with open(file_path, 'r', encoding='utf-8') as file:
        glossary_content = file.read()

    entries = glossary_content.split('**')[1:]  # Split by bolded entry titles
    dataset = set()

    for i in range(0, len(entries), 2):
        term = entries[i].strip()
        details = entries[i + 1]

        # Extract different surface forms
        surface_forms_match = re.search(r'_Surface forms_:\s*(.*?)\n', details)
        surface_forms = surface_forms_match.group(1).split('; ') if surface_forms_match else [term]

        # Extract covert meaning
        covert_meaning_match = re.search(r'_Covert \(in-group\) meaning_:\s*(.*?)\n', details)
        covert_meaning = covert_meaning_match.group(1) if covert_meaning_match else "Unknown"

        # Extract example context or use a generic sentence
        example_context_match = re.search(r'Example context.*?\n\s*(.*?)(?=\n\S|\Z)', details, re.DOTALL)
        example_context = example_context_match.group(1).strip() if example_context_match else f"The term '{term}' is used in various contexts."

        # Create dataset entries
        for surface_form in surface_forms:
            input_text = clean_text(example_context.replace(term, surface_form))
            output_text = clean_text(covert_meaning)
            dataset.add((input_text, output_text))

    return list(dataset)  # Convert set to list for CSV writing

# Running the parsing function on the glossary
file_path = 'dogwhistlegloss.md'
parsed_dataset = parse_glossary(file_path)

# Writing dataset to CSV
csv_file = 'dogwhistle_dataset.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Input', 'Output'])  # Header
    for input_text, output_text in parsed_dataset:
        writer.writerow([input_text, output_text])

print(f"Dataset with {len(parsed_dataset)} unique entries has been saved to {csv_file}.")
