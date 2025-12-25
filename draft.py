
from typing import List, Dict, Any
import sys
import expstats as es

sys.path.append('../FinalProjectCLI')
import expstats as es


if __name__ == "__main__":
    print(len(sys.argv))
    for arg in sys.argv:
        print(arg)
        
    if len(sys.argv) < 2:
        print("Usage: python draft.py <command> [<args>...]")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "list_participants":
        path = sys.argv[2]
        participants = es.list_participants(path)
        if participants is None:
            print("No participants found.")
        elif path != "":
            print(participants)

    elif command == "summary":
        csv_path = sys.argv[2]
        summary = es.compute_summary(csv_path)
        if summary is None:
            print("No data found.")
        
        print("Session summary:", summary)

    elif command == "load_session":
        csv_path = sys.argv[2]
        session = es._read_csv(csv_path)
        print("Session data:")
        for key, value in session.items():
            print(f"{key}: {value}")
    
    elif command == "compare_groups":
        csv_paths_a = sys.argv[2].split(",")
        csv_paths_b = sys.argv[3].split(",")
        comparison = es.compare_groups(csv_paths_a, csv_paths_b)
        print("Group comparison:", comparison)

    elif command == "generate_report":
        if len(sys.argv) < 4:
            print("Usage: python draft.py generate_report <csv_path> <out_path>")
            sys.exit(1)

        csv_path = sys.argv[2]
        out_path = sys.argv[3]

        summary = es.compute_summary(csv_path)
        es.generate_report(summary, out_path)
        print(f"Report generated at {out_path}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
