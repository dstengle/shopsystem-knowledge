# 0028 An argument refusal is raised with its command's prog and argparse's message

2026-09-27. `arguments.ArgumentRefused` carries the `prog` of the parser that refused and argparse's message, and lives in `arguments.py` because that module must not import `cli`. `cli._parsed` turns it into a `Refused` over one `Fault` (artifact the `prog`, message argparse's) so the one `_refuse` call in `main` prints it and `_refuse(` stays at two occurrences. Decision only; the line itself is adrs/0023.
