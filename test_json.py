from jsonschema import validate
jsonstring = {
    "title": "Medium: Count the Frequency of Words in a Sentence",
    "description": "Write a function `word_frequency` that takes in a sentence as input and returns a dictionary where keys are unique words from the sentence, and values are their respective frequencies. Ignore punctuation and convert all words to lowercase.\n\n#### Function Signature\n```python\ndef word_frequency(sentence: str) -> dict:\n```\n\n#### Input\n- `sentence` (str): A string that may contain letters, spaces, and punctuation.\n\n#### Output\n- Returns a dictionary where keys are unique words from the sentence in lowercase, and values are their respective frequencies.",
    "code": "import string\ndef word_frequency(sentence: str) -> dict:\n    # Remove punctuation\n    sentence = sentence.translate(str.maketrans('', '', string.punctuation))\n    # Convert to lowercase and split into words\n    words = sentence.lower().split()\n    # Count the frequency of each word\n    freq_dict = {word: words.count(word) for word in set(words)}\n    return freq_dict",
    "tests": ['assert word_frequency("Hello, hello, how are you?") == {"hello": 2, "how": 1, "are": 1, "you": 1}', 'assert word_frequency("This is a test sentence.") == {"this": 1, "is": 1, "a": 1, "test": 1, "sentence": 1}']
   }
 
schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "code": {"type": "string"},
            "tests": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["title", "description", "code", "tests"]
    }
  
validate(instance=jsonstring, schema=schema, )