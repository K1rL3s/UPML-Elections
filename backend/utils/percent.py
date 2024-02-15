def round_percents(percents: list[int]) -> list[int]:
    rounded_numbers = [round(num, 1) for num in percents]
    total = sum(rounded_numbers)

    if total < 100:
        difference = 100 - total
        min_index = rounded_numbers.index(min(rounded_numbers))
        rounded_numbers[min_index] += difference
    elif total > 100:
        difference = total - 100
        max_index = rounded_numbers.index(max(rounded_numbers))
        rounded_numbers[max_index] -= difference

    return rounded_numbers
