# graphion.py - Graphion interpreter
# Run with: python graphion.py [optional_script.gph]

import random

# Dictionary to store variables
variables = {}

# Command history (used for saving sessions)
history = []

# ------------------------------
# Helper functions
# ------------------------------

def get_value(expr):
    expr = expr.strip()
    if expr in variables:
        return variables[expr]
    elif expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    else:
        return expr

def eval_expr(expr):
    expr = expr.strip()
    if expr.startswith("round "):
        return round(float(get_value(expr[6:])))
    elif expr.startswith("random "):
        parts = expr[7:].split()
        return random.randint(int(parts[0]), int(parts[1]))
    else:
        val = get_value(expr)
        try:
            return float(val)
        except:
            return val

def run_block(lines):
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(" to ", 1)
        if len(parts) == 2:
            var = parts[0].strip()
            value = eval_expr(parts[1].strip())
            variables[var] = value
        elif line.startswith("say "):
            msg = line[4:].strip()
            if msg.startswith('"') and msg.endswith('"'):
                msg = msg[1:-1]
            elif msg in variables:
                msg = str(variables[msg])
            print(msg)
        elif line.startswith("ask "):
            # syntax: ask "Question?" and set var
            if "and set" in line:
                q, var = line.split("and set")
                q = q[4:].strip()
                if q.startswith('"') and q.endswith('"'):
                    q = q[1:-1]
                user_input = input(q + " ")
                var = var.strip()
                variables[var] = user_input
        elif line.startswith("repeat "):
            # repeat N times do
            parts = line.split()
            times = int(eval_expr(parts[1]))
            # assume next lines are indented or passed as a block
            print("Repeat blocks in scripts are only supported when running from .gph files")
        # Add more commands here as needed

# ------------------------------
# REPL
# ------------------------------

def repl():
    print("Graphion REPL. Type 'exit' to quit. Type 'save FILENAME' to save session.")
    while True:
        line = input(">>> ").strip()
        if line == "exit":
            break
        elif line.startswith("save "):
            filename = line[5:].strip()
            try:
                with open(filename + ".gph", "w") as f:
                    f.write("\n".join(history))
                print(f"Session saved as {filename}.gph")
            except Exception as e:
                print("Error saving file:", e)
        elif line.startswith("run "):
            filename = line[4:].strip()
            try:
                with open(filename, "r") as f:
                    script_lines = f.readlines()
                run_block(script_lines)
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
        else:
            run_block([line])
            history.append(line)

# ------------------------------
# Main
# ------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r") as f:
                script_lines = f.readlines()
            run_block(script_lines)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
    else:
        repl()
