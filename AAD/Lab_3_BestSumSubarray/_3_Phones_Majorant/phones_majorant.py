def find_majorant_hacker_2(phone_numbers: list[str], start, end) -> str | None:
    if end - start == 1:
        return phone_numbers[start]

    else:
        mid = (start + end) // 2
        half_length = (end - start) // 2

        candidate_1 = find_majorant_hacker_2(phone_numbers, start, mid)
        candidate_2 = find_majorant_hacker_2(phone_numbers, mid, end)

        if candidate_1 is not None and check_same_device(candidate_1, candidate_2):
            return candidate_1

        stats_candidate_1 = 0
        stats_candidate_2 = 0

        for i in range(start, end):
            if check_same_device(candidate_1, phone_numbers[i]):
                stats_candidate_1 += 1
                if stats_candidate_1 > half_length:
                    return candidate_1

            elif check_same_device(candidate_2, phone_numbers[i]):
                stats_candidate_2 += 1
                if stats_candidate_2 > half_length:
                    return candidate_2

        return None


def find_majorant_hacker_3(phone_numbers: list[str], start, end) -> list[str]:
    if end - start == 1:
        return phone_numbers[start:end]

    else:
        mid = (start + end) // 2
        third_part_length = (end - start) // 3

        list_candidates_1 = find_majorant_hacker_3(phone_numbers, start, mid)
        list_candidates_2 = find_majorant_hacker_3(phone_numbers, mid, end)

        merged_candidates = list_candidates_1 + list_candidates_2
        unique_candidates: dict[str, int] = {}

        # Deduplication of candidates
        for current_candidate in merged_candidates:
            is_already_in_list = False
            for accepted_candidate in unique_candidates:
                if check_same_device(current_candidate, accepted_candidate):
                    is_already_in_list = True
                    break

            if not is_already_in_list:
                unique_candidates[current_candidate] = 0

        # Counting votes
        for i in range(start, end):
            for candidate in unique_candidates.keys():
                if check_same_device(candidate, phone_numbers[i]):
                    unique_candidates[candidate] += 1
                    break # Optimization: one number belongs to only one device

        # Filtering winners
        win_list = [phone for phone, stats in unique_candidates.items() if stats > third_part_length]

        return win_list





def check_same_device(phone_a: str | None, phone_b: str | None) -> bool:
    if phone_a is None or phone_b is None:
        return False
    return db[phone_a] == db[phone_b]


if __name__ == "__main__":
    db = {
        "+380671110001": "IMEI_FRAUD_PRIMARY",
        "+380671110002": "IMEI_FRAUD_PRIMARY",
        "+380671110003": "IMEI_FRAUD_PRIMARY",
        "+380671110004": "IMEI_FRAUD_PRIMARY",
        "+380671110005": "IMEI_FRAUD_PRIMARY",
        "+380671110006": "IMEI_FRAUD_PRIMARY",
        "+380671110007": "IMEI_FRAUD_PRIMARY",
        "+380671110008": "IMEI_FRAUD_PRIMARY",
        "+380671110009": "IMEI_FRAUD_PRIMARY",
        "+380671110010": "IMEI_FRAUD_PRIMARY",

        "+380502220001": "IMEI_FRAUD_SECONDARY",
        "+380502220002": "IMEI_FRAUD_SECONDARY",
        "+380502220003": "IMEI_FRAUD_SECONDARY",

        "+380933330001": "IMEI_LEGIT_USER_1",
        "+380933330002": "IMEI_LEGIT_USER_2",
        "+380933330003": "IMEI_LEGIT_USER_3",
    }

    phone_numbers = [
        "+380671110001",
        "+380502220001",
        "+380671110002",
        "+380933330001",
        "+380671110003",
        "+380502220002",
        "+380671110004",
        "+380671110005",
        "+380933330002",
        "+380671110006",
        "+380502220003",
        "+380671110007",
        "+380671110008",
        "+380933330003",
        "+380671110009",
        "+380671110010",
        "+380671110001",
        "+380671110002",
    ]

    # Testing for N/2 threshold
    majorant_n2 = find_majorant_hacker_2(phone_numbers, 0, len(phone_numbers))
    print("--- Testing for N/2 threshold ---")
    if majorant_n2:
        print(f"Device found! One of its numbers: {majorant_n2} (IMEI: {db[majorant_n2]})")
    else:
        print(r"No devices found that made > 50% of the calls.")

    print("\n--- Testing for N/3 threshold ---")
    # Testing for N/3 threshold
    majorant_n3 = find_majorant_hacker_3(phone_numbers, 0, len(phone_numbers))
    if majorant_n3:
        for num in majorant_n3:
            print(f"Device found! One of its numbers: {num} (IMEI: {db[num]})")
    else:
        print(r"No devices found that made > 33.3% of the calls.")