def process_text_chunks(clean_text, chunk_size=500):
    """
    Splits cleaned text into chunks of specified size.

    Parameters:
    - clean_text: str, the text to split
    - chunk_size: int, the number of words per chunk

    Returns:
    - list of str: List of text chunks
    """
    words = clean_text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks
