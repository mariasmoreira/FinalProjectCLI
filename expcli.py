# @Ficheiro: expcli.py
# @Autor: Maria S. Moreira
# @Data: 26/12/2025

from typing import List, Dict, Any
import sys
import argparse
import expstats as es
import tomli
import os

VERSION = "1.0.0"

""" Command line interface for experimental statistics 
    Structure of the commands: first argument is the command,
    second argument is the path to the CSV file or directory,
    third argument (if needed) is the output path for generate_report command."""

# Minimal argparse handling for global flags
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="store_true", help="Mostra ajuda")
parser.add_argument("-v", "--verbose", action="store_true", help="Modo detalhado")
parser.add_argument("--version", action="version", version=f"expcli {VERSION}")

# Parse only known flags
args, unknown = parser.parse_known_args()

if args.help:  # If help flag is provided, show usage information
    print("Uso: python expcli.py <command> [<args>...]")
    print("Comandos disponíveis: list_participants, summary, compare_groups, generate_report")
    print("Estrutura dos comandos : <command> <path_to_csv_or_directory> [<output_path>]")
    print("Flags globais:")
    print("  -h, --help     Mostra ajuda")
    print("  -v, --verbose  Modo detalhado")
    print("  --version      Mostra versão")
    print("--config <path>  Especifica o caminho do arquivo de configuração (padrão: config.toml)")
    sys.exit(0)

verbose = args.verbose  
if verbose:   # If verbose flag is set, print original arguments
    print("[VERBOSE] Argumentos originais:", sys.argv)


config_path = "config.toml"
if "--config" in sys.argv: # If config flag is provided, get the config path
    config_index = sys.argv.index("--config")  # Find index of --config
    if len(sys.argv) > config_index + 1:  # Check if there is a path after --config
        config_path = sys.argv[config_index + 1]  # Get config path from arguments
        sys.argv.pop(config_index)  # Remove --config from arguments
        sys.argv.pop(config_index)  # Remove config path from arguments
    else:
        print("Erro: --config flag requires a path argument.")
        sys.exit(1)   # Exit if no path is provided

config = {}
if os.path.exists(config_path):  # Check if config file exists
    with open(config_path, "rb") as f:
        config = tomli.load(f)  # Load configuration from TOML file
    if verbose:
        print(f"[VERBOSE] Configuração carregada de {config_path}: {config}")
    else:
        if "--config" in sys.argv:
            print(f"Arquivo de configuração {config_path} não encontrado.")
            sys.exit(1)  # Exit if config file is not found and --config was specified

default_datadir = config.get("paths", {}).get("default_datadir", "data/")
default_ext = config.get("report", {}).get("default_ext", "txt")
include_summ = config.get("report", {}).get("include_summ", True)


if __name__ == "__main__": # Main entry point for the CLI
    print(len(sys.argv))  # Check number of arguments
    for arg in sys.argv:
        print(arg)    # Print each argument
        
    if len(sys.argv) < 2:   # Ensure the minimum number of arguments
        print("Usage: python expcli.py <command> [<args>...]")
        sys.exit(1)
    
    command = sys.argv[1]  # First argument is the command

    if command == "list_participants": # List participants command
        path = sys.argv[2] if len(sys.argv) > 2 else default_datadir # Second argument is the path
        participants = es.list_participants(path)
        if participants is None:
            print("No participants found.") # Handle no participants case
        elif len(sys.argv) < 3:
            print("Usage: python expcli.py list_participants <data_dir>") # Check if the necessary arguments are provided
            sys.exit(1)
        
        print(participants)

    elif command == "summary":
        csv_path = sys.argv[2] if len(sys.argv) > 2 else default_datadir
        summary = es.compute_summary(csv_path)
        if summary is None:
            print("No data found.") # Handle no data case
        elif len(sys.argv) < 3:
            print("Usage: python expcli.py summary <csv_path>") # Check if the necessary arguments are provided
            sys.exit(1)
        
        print("Session summary:", summary)

    
    elif command == "compare_groups":
        csv_paths_a = sys.argv[2].split(",") # Cannot be configurated in config file due to multiple paths
        csv_paths_b = sys.argv[3].split(",") # Cannot be configurated in config file due to multiple paths
        comparison = es.compare_groups(csv_paths_a, csv_paths_b)
        if comparison is None:
            print("No data found.") # Handle no data case
        elif len(sys.argv) < 4:
            print("Usage: python expcli.py compare_groups <csv_paths_a> <csv_paths_b>")
            sys.exit(1)
            
        print("Group comparison:", comparison)

    elif command == "generate_report":
        if len(sys.argv) < 4: # Cannot be configurated in config file due to multiple paths
            print("Usage: python expcli.py generate_report <csv_path> <out_path>") # Check if the necessary arguments are provided
            sys.exit(1)

        csv_path = sys.argv[2] if len(sys.argv) > 3 else f"report.{default_ext}"
        out_path = sys.argv[3] if len(sys.argv) > 3 else f"report.{default_ext}"

        summary = es.compute_summary(csv_path)
        es.generate_report(summary, out_path)
        print(f"Report generated at {out_path}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    