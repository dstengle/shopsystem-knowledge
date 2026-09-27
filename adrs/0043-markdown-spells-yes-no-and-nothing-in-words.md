# 0043 A markdown page spells a yes, a no and an empty value in words

2026-09-27. Fills in 0038 and 0041. On a markdown page a yes is `yes`, a no is `no`, and an empty value is nothing: the field's name and its colon with nothing after them in the field list (`- **owner**:`), an empty cell in a table, nothing between the separators where it sits inline. `True`, `False`, `None`, `true`, `false` and `null` never appear as a value. The user chose this reading of the spec's "no value is ever printed as a programming language's representation of it" over keeping YAML's own spelling.
