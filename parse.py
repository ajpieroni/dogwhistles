import re

# clean text function
def clean_text(text):
    """Function to clean the text data."""
    text = text.strip()  # Trim white spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\\', '', text)  # Remove backslashes
    # remove quotes
    text = re.sub(r'"', '', text)
    # Add any additional cleaning steps here if needed
    return text

def parse_glossary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    entries = content.split('**')[1:]  # Split by bolded entry titles

    dataset = []
    skipped_entries = 0

    for i in range(0, len(entries), 2):
        term = entries[i].strip()
        details = entries[i + 1]

        # Extracting surface forms as a list
        surface_forms_match = re.search(r'_Surface forms_:\s*(.*?)\n', details)
        surface_forms = surface_forms_match.group(1).split('; ') if surface_forms_match else [term]

        # Extracting covert meaning
        covert_meaning_match = re.search(r'_Covert \(in-group\) meaning_:\s*(.*?)\n', details)
        covert_meaning = covert_meaning_match.group(1) if covert_meaning_match else "Unknown"

        # Adjusting the regex for extracting example context
        example_context_match = re.search(r'Example context.*?\n\s*(.*?)(?=\n\S)', details, re.DOTALL)
        example_context = example_context_match.group(1).strip() if example_context_match else None

        if not example_context:
            skipped_entries += 1
            continue

        # Creating formatted training pairs
        for surface_form in surface_forms:
            input_text = clean_text(example_context.replace(term, surface_form))
            output_text = clean_text(covert_meaning)
            formatted_pair = f"Input: {input_text}\nOutput: {output_text}\n"
            dataset.append(formatted_pair)

    return dataset, skipped_entries

# Example usage
file_path = 'dogwhistlegloss.md'

parsed_dataset, skipped_entries = parse_glossary(file_path)

# Diagnostic message
print(f"Skipped {skipped_entries} entries due to missing example contexts.")
print(f"Processed {len(parsed_dataset)} entries.")
# print length of the entries
print(len(parsed_dataset))

# Print the first few formatted pairs for review
for pair in parsed_dataset[:10]:
    print(pair)
