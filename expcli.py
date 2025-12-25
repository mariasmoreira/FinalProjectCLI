# @Ficheiro: expcli.py
# @Autor: Maria S. Moreira
# @Data: 26/12/2025

""" Dependencies and imports """
from typing import List, Dict, Any
import sys
import expstats as es

""" Command line interface for experimental statistics 
    Structure of the commands: firt argument is the command,
    second argument is the path to the CSV file or directory,
    third argument (if needed) is the output path for genereate_report command."""

if __name__ == "__main__": # Main entry point for the CLI
    print(len(sys.argv))  # Check number of arguments
    for arg in sys.argv:
        print(arg)    # Print each argument
        
    if len(sys.argv) < 2:   # Ensure the minimum number of arguments
        print("Usage: python draft.py <command> [<args>...]")
        sys.exit(1)
    
    command = sys.argv[1]  # First argument is the command

    if command == "load_session":
        csv_path = sys.argv[2]
        session = es._read_csv(csv_path)
        if session is None:
            print("No data found.") # Handle no data case
        elif len(sys.argv) < 3:
            print("Usage: python draft.py load_session <csv_path>") # Check if the necessary arguments are provided
            sys.exit(1)

        print("Session data:")
        for key, value in session.items(): # for each key-value pair in session, print them
            print(f"{key}: {value}")

    if command == "list_participants": # List participants command
        path = sys.argv[2] # Second argument is the path
        participants = es.list_participants(path)
        if participants is None:
            print("No participants found.") # Handle no participants case
        elif len(sys.argv) < 3:
            print("Usage: python draft.py list_participants <data_dir>") # Check if the necessary arguments are provided
            sys.exit(1)
        
        print(participants)

    elif command == "summary":
        csv_path = sys.argv[2]
        summary = es.compute_summary(csv_path)
        if summary is None:
            print("No data found.") # Handle no data case
        elif len(sys.argv) < 3:
            print("Usage: python draft.py summary <csv_path>") # Check if the necessary arguments are provided
            sys.exit(1)
        
        print("Session summary:", summary)

    
    elif command == "compare_groups":
        csv_paths_a = sys.argv[2].split(",")
        csv_paths_b = sys.argv[3].split(",")
        comparison = es.compare_groups(csv_paths_a, csv_paths_b)
        if comparison is None:
            print("No data found.") # Handle no data case
        elif len(sys.argv) < 4:
            print("Usage: python draft.py compare_groups <csv_paths_a> <csv_paths_b>")
            sys.exit(1)
            
        print("Group comparison:", comparison)

    elif command == "generate_report":
        if len(sys.argv) < 4:
            print("Usage: python draft.py generate_report <csv_path> <out_path>") # Check if the necessary arguments are provided
            sys.exit(1)

        csv_path = sys.argv[2]
        out_path = sys.argv[3]

        summary = es.compute_summary(csv_path)
        es.generate_report(summary, out_path)
        print(f"Report generated at {out_path}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
