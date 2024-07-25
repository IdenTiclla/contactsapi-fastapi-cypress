def example_function_1(a: int, b: int) -> int:
    return a + b

def main():
    r = example_function_1(1, 2)
    print(r)
    print(r.bit_length)


if __name__ == "__main__":
    main()
