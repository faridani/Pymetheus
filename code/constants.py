template = {
  "title": "Title for the problem (for example: Palindrome Checker)",
  "description": "A description of the problem in string form, the description may contain function signature, input format, output format, constraints and hints. Example: A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization). Write a function `is_palindrome` that checks if a given string is a palindrome.\n\n#### Function Signature\n```python\ndef is_palindrome(s: str) -> bool:\n```\n\n#### Input\n- `s` (str): A string that may contain letters, numbers, spaces, and punctuation.\n\n#### Output\n- Returns `True` if the input string is a palindrome, `False` otherwise.\n",
   "code": "import string\n\ndef is_palindrome(s: str) -> bool:\n    # Convert to lowercase\n    s = s.lower()\n    # Remove non-alphanumeric characters\n    s = ''.join(char for char in s if char in string.ascii_letters + string.digits)\n    # Check if the string reads the same forwards and backwards\n    return s == s[::-1]\n",
  "tests": [
    "assert is_palindrome(\"A man, a plan, a canal, Panama\") == True",
    "assert is_palindrome(\"racecar\") == True",
    "assert is_palindrome(\"hello\") == False",
    "assert is_palindrome(\"No 'x' in Nixon\") == True"
  ]
}

difficulties = ["easy", "medium", "hard", "super hard", "insanely difficult"]

styles = ["LeetCode", "CodeSignal", "HackerRank", "CodeWars", "Project Euler", "Daily Coding Problem", 
                  "Interview Query", "Exercism", "Codecademy", "Codewars", "Internationals Olympiad", "Google Code Jam", 
                  "Facebook Hacker Cup", "Codeforces", "AtCoder", "TopCoder", "Competitive Programming", "ICPC", 
                  "ACM-ICPC", "CodeChef", "HackerEarth", "SPOJ"]