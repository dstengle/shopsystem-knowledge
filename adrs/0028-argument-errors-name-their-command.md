# 0028 An argument refusal is raised with its command's prog and argparse's message

2026-09-27. `arguments.ArgumentRefused` carries the `prog` of the parser that refused and argparse's message, and `cli._parsed` turns it into a `Refused` over one `Fault` (artifact the `prog`, message argparse's).
