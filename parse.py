import re

def parse_glossary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    entries = content.split('**')[1:]  # Split by bolded entry titles

    dataset = []

    for i in range(0, len(entries), 2):
        term = entries[i].strip()
        details = entries[i + 1]

        # Extracting surface forms as a list
        surface_forms_match = re.search(r'_Surface forms_:\s*(.*?)\n', details)
        surface_forms = surface_forms_match.group(1).split('; ') if surface_forms_match else [term]

        # Extracting covert meaning
        covert_meaning_match = re.search(r'_Covert \(in-group\) meaning_:\s*(.*?)\n', details)
        covert_meaning = covert_meaning_match.group(1) if covert_meaning_match else "Unknown"

        # Extracting example context
        example_context_match = re.search(r'Example context \(in \[.*?\]\(.*?\)\)\s*\n\s*(.*?)\n', details)
        example_context = example_context_match.group(1) if example_context_match else None

        # Creating training pairs
        for surface_form in surface_forms:
            if example_context:
                input_text = example_context.replace(term, surface_form)
            else:
                # Create a generic sentence if no context is provided
                input_text = f"This statement includes the term '{surface_form}'."

            output_text = covert_meaning
            dataset.append((input_text, output_text))

    return dataset

# Example usage
file_path = 'dogwhistlegloss.md'

parsed_dataset = parse_glossary(file_path)

# Print the first 100 input-output pairs
for input_text, output_text in parsed_dataset[:100]:
    print(f"Input: {input_text}\nOutput: {output_text}\n")
