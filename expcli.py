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
def main() -> None:
    """Arguments parsing and command dispatching"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Mostra ajuda")
    parser.add_argument("-v", "--verbose", action="store_true", help="Modo detalhado")
    parser.add_argument("--version", action="version", version=f"expcli {VERSION}")
# Parse only known flags
    args, unknown = parser.parse_known_args() # Parse known arguments
    verbose = args.verbose   # If verbose flag is set, print original arguments

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

 
    if verbose:   # If verbose flag is set, print original arguments
        print("[VERBOSE] Argumentos originais:", sys.argv)

    """Load configuration from TOML file"""
    config_path = "config.toml"
    if "--config" in sys.argv: # If config flag is provided, get the config path
        config_index = sys.argv.index("--config")  # Find index of --config
        if len(sys.argv) > config_index + 1:  # Check if there is a path after --config
            config_path = sys.argv[config_index + 1]  # Get config path from arguments
            sys.argv.pop(config_index)  # Remove --config from arguments
            sys.argv.pop(config_index)  # Remove config path from arguments
        else:
            print("Erro: --config flag necessita de um caminho.")
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

    default_datadir = config.get("diretórios", {}).get("default_datadir", "data/")
    default_ext = config.get("report", {}).get("default_ext", "txt")
    include_summ = config.get("report", {}).get("include_summ", True)


   
    """Check and dispatch commands"""  
    if len(sys.argv) < 2:   # Ensure the minimum number of arguments
        print("Uso: python expcli.py <command> [<args>...]")
        sys.exit(1)
    
    command = sys.argv[1]  # First argument is the command
    """ if statements for each command """
    if command == "list_participants": # List participants command
        if len(sys.argv) < 3:
            print("Uso: python expcli.py list_participants <csv_path>") # Check if the necessary arguments are provided
            sys.exit(1)
        path = sys.argv[2] if len(sys.argv) > 2 else default_datadir  
        participants = es.list_participants(path)
        if not os.path.exists(path):
            print(f"Diretório {path} não existe.")  # Handle directory not found case
            sys.exit(1)
        if not participants:
            print("Nenhum participante encontrado.") # Handle no participants case
            sys.exit(1)
        for p in sorted(participants):  # Print sorted list of participants
            print(f"- {p}")

    elif command == "summary":
        csv_path = sys.argv[2] if len(sys.argv) > 2 else default_datadir
        if not os.path.exists(csv_path):
            print(f"Arquivo {csv_path} não encontrado.")
            sys.exit(1)

        try:    # Handle traceback for file not found or processing errors
            summary = es.compute_summary(csv_path)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao processar o CSV: {e}")
            sys.exit(1)
        
        print("Session summary:", summary)
    
    elif command == "compare_groups":
        if len(sys.argv) < 4:
            print("Uso: python expcli.py compare_groups <csv_paths_a> <csv_paths_b>") # Check if the necessary arguments are provided
            sys.exit(1)
        csv_paths_a = sys.argv[2].split(",") # Cannot be configurated in config file due to multiple paths
        csv_paths_b = sys.argv[3].split(",") # Cannot be configurated in config file due to multiple paths
        
        for f in csv_paths_a + csv_paths_b:  # Check if all files exist
            if not os.path.exists(f):
                print(f"Arquivo {f} não encontrado.")
                sys.exit(1)
       
        try :   #Handle traceback for file not found or processing errors
            comparison = es.compare_groups(csv_paths_a, csv_paths_b)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao comparar grupos: {e}")
            sys.exit(1)

        print("Comparação entre grupos:", comparison)

    elif command == "generate_report":
        if len(sys.argv) < 4: # Cannot be configurated in config file due to multiple paths
            print("Uso: python expcli.py generate_report <csv_path> <out_path>") # Check if the necessary arguments are provided
            sys.exit(1)

        csv_path = sys.argv[2] if len(sys.argv) > 3 else f"report.{default_ext}"
        out_path = sys.argv[3] if len(sys.argv) > 3 else f"report.{default_ext}"
        

        
        if not os.path.exists(csv_path):  # Check if input CSV file exists
            print(f"Arquivo {csv_path} não encontrado.")
            sys.exit(1)
        if os.path.exists(out_path):  # If itput file exists, ask for overwrite confirmation
            resp = input(f"O arquivo {out_path} já existe. Sobrescrever? (s/n): ")
            if resp.lower() != "s":
                print("Operação cancelada.")
                sys.exit(0)
        
        summary = es.compute_summary(csv_path)
        es.generate_report(summary, out_path)
        print(f"Relatório gerado em {out_path}")

    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)

if __name__ == "__main__": # Run the main function
    main()   