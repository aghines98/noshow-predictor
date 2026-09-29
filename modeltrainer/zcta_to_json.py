import csv
import json
import sys


def convert_zipcode_data_to_json(input_file: str, output_file: str):
    """
    Reads a pipe-delimited file and converts it to JSON.

    Args:
        input_file: Path to the input text file
        output_file: Path to the output JSON file
    """
    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')

        for row in reader:
            entry = {
                'geoId': row['GEOID'],
                'landSquareMiles': float(row['ALAND_SQMI']),
                'centroidLatitude': float(row['INTPTLAT']),
                'centroidLongitude': float(row['INTPTLONG'])
            }
            results.append(entry)

    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"Converted {len(results)} records to {output_file}")
    return results


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python zcta_to_json.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = convert_zipcode_data_to_json(input_file, output_file)

    # Print first record as sample
    if data:
        print("\nSample record:")
        print(json.dumps(data[0], indent=2))