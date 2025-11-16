import csv
import json
import argparse

# Example calling script
# python3 csv_converter.py employees.csv employeeId --type_name Employee --is_identity --output employees2.json

# Converts a CSV file to a JSON structure compatible with IndyKite.
#    
# Args:
#  csv_file_path (str): Path to the input CSV file.
#  external_id_col (str): Name of the column to use as external_id.
#  type_name (str): The type of the entity (e.g., "Employee", "Book").
#  is_identity (bool): Flag to set for all nodes.
#  output_file (str): Output JSON file path.

def csv_to_json(csv_file_path, external_id_col, type_name="Entity", is_identity=False, output_file="output.json"):

    nodes = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            external_id = row[external_id_col]
            
            # Build properties excluding the external_id column
            properties = []
            for key, value in row.items():
                if key != external_id_col:
                    properties.append({
                        "type": key,
                        "value": value
                    })

            node = {
                "external_id": external_id,
                "type": type_name,
                "is_identity": is_identity,
                "properties": properties
            }
            nodes.append(node)
    
    output_data = {"nodes": nodes}

    # Write JSON output
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"JSON file saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file to IndyKite-compatible JSON.")
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument("external_id_col", help="Column name to use as external_id")
    parser.add_argument("--type_name", default="Entity", help="Type of the entity (default: Entity)")
    parser.add_argument("--is_identity", action="store_true", help="Set if nodes are identities")
    parser.add_argument("--output", default="output.json", help="Output JSON file path (default: output.json)")

    args = parser.parse_args()

    csv_to_json(
        csv_file_path=args.csv_file,
        external_id_col=args.external_id_col,
        type_name=args.type_name,
        is_identity=args.is_identity,
        output_file=args.output
    )


if __name__ == "__main__":
    main()