import re

def separate_and_number(lst):
    joined_str = ' '.join(lst)
    chunks = joined_str.split('EOA')
    chunks = [chunk.strip('-').strip() for chunk in chunks if chunk.strip()]
    return chunks

def extract_number_and_clean(chunks):
    processed_chunks = []
    for chunk in chunks:
        match = re.match(r'^(\d+)\s*[)\.]?\s*(.*)', chunk)
        if match:
            number, content = match.groups()
            processed_chunks.append((int(number), content.strip()))
        else:
            processed_chunks.append((None, chunk.strip()))
    return processed_chunks

def pre_process(input_list):
    data = {}
    separated_chunks = separate_and_number(input_list)
    numbered_chunks = extract_number_and_clean(separated_chunks)
    for number, content in numbered_chunks:
        if number is not None:
            data[str(number)]=content
        else:
            data[str("None")]=content
    return data
