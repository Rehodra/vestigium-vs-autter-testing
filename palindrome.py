def is_palindrome(text: str) -> bool:
    """Check if the given text is a palindrome."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def main():
    user_input = input("Enter a string: ")
    if is_palindrome(user_input):
        print(f'"{user_input}" is a palindrome!')
    else:
        print(f'"{user_input}" is not a palindrome.')


if __name__ == "__main__":
    main()

