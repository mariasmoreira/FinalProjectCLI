
"""
expstats.py
Módulo de apoio ("caixa preta") para análise de experiências simples de tempo de reação.

Formato esperado dos ficheiros CSV:
- Colunas obrigatórias (header):
    participant_id, condition, trial, rt, correct

Onde:
- participant_id: string identificadora da/o participante (ex: "P001")
- condition: string identificadora da condição/grupo (ex: "A", "B")
- trial: número inteiro do trial (1, 2, 3, ...)
- rt: tempo de reação em milissegundos (número real)
- correct: 1 se a resposta foi correta, 0 se incorreta

Os ficheiros de exemplo seguem este formato.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import csv
import os
import glob
import statistics


@dataclass
class SessionData:
    participant_id: str
    condition: str
    trials: int
    valid_trials: int
    rts: List[float]
    correct_flags: List[int]


def _read_csv(csv_path: str) -> SessionData:
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Ficheiro não encontrado: {csv_path}")

    rts: List[float] = []
    correct_flags: List[int] = []
    participant_id = None
    condition = None
    trials = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_cols = {"participant_id", "condition", "trial", "rt", "correct"}
        if not required_cols.issubset(reader.fieldnames or []):
            raise ValueError(
                f"Ficheiro {csv_path} não tem as colunas obrigatórias: {', '.join(sorted(required_cols))}"
            )
        for row in reader:
            trials += 1
            participant_id = participant_id or row["participant_id"]
            condition = condition or row["condition"]
            try:
                rt = float(row["rt"])
                correct = int(row["correct"])
                rts.append(rt)
                correct_flags.append(correct)
            except Exception as e:
                # Ignora linhas mal formatadas
                continue

    if participant_id is None or condition is None or len(rts) == 0:
        raise ValueError(f"Ficheiro {csv_path} não contém dados válidos.")

    return SessionData(
        participant_id=participant_id,
        condition=condition,
        trials=trials,
        valid_trials=len(rts),
        rts=rts,
        correct_flags=correct_flags,
    )


def load_session(csv_path: str) -> Dict[str, Any]:
    """
    Lê um ficheiro CSV de sessão e devolve um dicionário com os dados e metadados.
    """
    session = _read_csv(csv_path)
    return {
        "participant_id": session.participant_id,
        "condition": session.condition,
        "trials": session.trials,
        "valid_trials": session.valid_trials,
        "rts": session.rts,
        "correct_flags": session.correct_flags,
    }


def list_participants(data_dir: str) -> List[str]:
    """
    Devolve a lista de IDs de participantes encontrados nos CSVs de um diretório.
    Usa a coluna participant_id do próprio ficheiro.
    """
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Diretório não encontrado: {data_dir}")

    participants = set()
    pattern = os.path.join(data_dir, "*.csv")
    for path in glob.glob(pattern):
        try:
            sess = _read_csv(path)
            participants.add(sess.participant_id)
        except Exception:
            # Ignora ficheiros inválidos
            continue

    return sorted(participants)


def compute_summary(csv_path: str) -> Dict[str, Any]:
    """
    Calcula estatísticas descritivas (médias, desvios padrão, número de trials válidos,
    percentagem de erros, etc.) para uma sessão.
    """
    session = _read_csv(csv_path)
    mean_rt = statistics.mean(session.rts)
    sd_rt = statistics.pstdev(session.rts) if len(session.rts) > 1 else 0.0
    errors = sum(1 for c in session.correct_flags if c == 0)
    error_rate = (errors / session.valid_trials) * 100.0 if session.valid_trials > 0 else 0.0

    return {
        "participant_id": session.participant_id,
        "condition": session.condition,
        "trials": session.trials,
        "valid_trials": session.valid_trials,
        "mean_rt": mean_rt,
        "sd_rt": sd_rt,
        "errors": errors,
        "error_rate": error_rate,
    }


def _aggregate_group(csv_paths: List[str]) -> Dict[str, Any]:
    all_rts: List[float] = []
    all_correct: List[int] = []
    conditions = set()
    n_sessions = 0

    for path in csv_paths:
        sess = _read_csv(path)
        n_sessions += 1
        all_rts.extend(sess.rts)
        all_correct.extend(sess.correct_flags)
        conditions.add(sess.condition)

    if n_sessions == 0 or len(all_rts) == 0:
        raise ValueError("Não foi possível agregar o grupo (sem sessões válidas).")

    mean_rt = statistics.mean(all_rts)
    sd_rt = statistics.pstdev(all_rts) if len(all_rts) > 1 else 0.0
    errors = sum(1 for c in all_correct if c == 0)
    error_rate = (errors / len(all_correct)) * 100.0 if all_correct else 0.0

    return {
        "n_sessions": n_sessions,
        "mean_rt": mean_rt,
        "sd_rt": sd_rt,
        "errors": errors,
        "error_rate": error_rate,
        "conditions": sorted(conditions),
    }


def compare_groups(csv_paths_a: List[str], csv_paths_b: List[str]) -> Dict[str, Any]:
    """
    Compara duas condições (A e B) e devolve métricas agregadas.
    """
    if not csv_paths_a or not csv_paths_b:
        raise ValueError("Ambos os grupos A e B devem ter pelo menos um ficheiro.")

    group_a = _aggregate_group(csv_paths_a)
    group_b = _aggregate_group(csv_paths_b)

    diff_mean_rt = group_b["mean_rt"] - group_a["mean_rt"]
    diff_error_rate = group_b["error_rate"] - group_a["error_rate"]

    return {
        "group_a": group_a,
        "group_b": group_b,
        "diff_mean_rt": diff_mean_rt,
        "diff_error_rate": diff_error_rate,
    }


def generate_report(summary: Dict[str, Any], out_path: str) -> None:
    """
    Gera um relatório de texto simples a partir de um dicionário de resultados.
    O dicionário pode ser o resultado de compute_summary() ou compare_groups().
    """
    lines: List[str] = []

    if "participant_id" in summary:
        # relatório de sessão individual
        lines.append(f"Relatório de sessão")
        lines.append(f"Participante: {summary.get('participant_id')}")
        lines.append(f"Condição: {summary.get('condition')}")
        lines.append(f"Trials totais: {summary.get('trials')}")
        lines.append(f"Trials válidos: {summary.get('valid_trials')}")
        lines.append(f"Tempo de reação médio: {summary.get('mean_rt'):.2f} ms")
        lines.append(f"Desvio padrão do TR: {summary.get('sd_rt'):.2f} ms")
        lines.append(f"Erros: {summary.get('errors')} ({summary.get('error_rate'):.2f}%)")
    elif "group_a" in summary and "group_b" in summary:
        # relatório de comparação de grupos
        ga = summary["group_a"]
        gb = summary["group_b"]
        lines.append("Relatório de comparação de grupos")
        lines.append("Grupo A:")
        lines.append(f"  Sessões: {ga['n_sessions']}")
        lines.append(f"  TR médio: {ga['mean_rt']:.2f} ms (SD={ga['sd_rt']:.2f})")
        lines.append(f"  Erros: {ga['errors']} ({ga['error_rate']:.2f}%)")
        lines.append("Grupo B:")
        lines.append(f"  Sessões: {gb['n_sessions']}")
        lines.append(f"  TR médio: {gb['mean_rt']:.2f} ms (SD={gb['sd_rt']:.2f})")
        lines.append(f"  Erros: {gb['errors']} ({gb['error_rate']:.2f}%)")
        lines.append("Diferenças (B - A):")
        lines.append(f"  Δ TR médio: {summary['diff_mean_rt']:.2f} ms")
        lines.append(f"  Δ taxa de erros: {summary['diff_error_rate']:.2f} pontos percentuais")
    else:
        lines.append("Resumo genérico:")
        for k, v in summary.items():
            lines.append(f"{k}: {v}")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
