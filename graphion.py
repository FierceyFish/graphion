import random
import os
from datetime import datetime  # Added for current_time

# ------------------------------
# Graphion Interpreter v1.4
# ------------------------------

variables = {}
functions = {}  # User-defined functions

# ------------------------------
# Helper Functions
# ------------------------------

def get_value(var):
    if isinstance(var, str) and var in variables:
        return variables[var]
    try:
        return float(var)
    except:
        return var

def eval_expr(expr):
    expr = expr.strip()
    if expr == "current_time":
        return datetime.now().strftime("%H:%M:%S")  # Native current_time
    if expr.startswith("uppercase "):
        return str(get_value(expr[10:])).upper()
    if expr.startswith("lowercase "):
        return str(get_value(expr[10:])).lower()
    if expr.startswith("round "):
        return round(float(get_value(expr[6:])))
    if expr.startswith("length "):
        val = get_value(expr[7:])
        return len(val) if isinstance(val, (list, str)) else 0
    if expr.startswith("join "):
        parts = expr[5:].split(" with ")
        lst = get_value(parts[0].strip())
        sep = parts[1].strip().strip('"')
        return sep.join(lst) if isinstance(lst, list) else str(lst)
    if expr.startswith("split "):
        parts = expr[6:].split(" by ")
        string = get_value(parts[0].strip())
        sep = parts[1].strip().strip('"')
        return string.split(sep)
    if expr.startswith("random "):
        nums = expr[7:].split()
        return random.randint(int(eval_expr(nums[0])), int(eval_expr(nums[1])))
    return get_value(expr)

# ------------------------------
# Phase 1: User-Defined Functions
# ------------------------------

def run_block(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        if line.startswith("make "):
            parts = line[5:].split(" with ")
            fname = parts[0].strip()
            params = []
            if len(parts) > 1:
                params = [p.strip() for p in parts[1].split(",")]
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != "end":
                body.append(lines[i])
                i += 1
            functions[fname] = {"params": params, "body": body}
        elif line.startswith("call "):
            parts = line[5:].split(" with ")
            fname = parts[0].strip()
            args = []
            if len(parts) > 1:
                args = [eval_expr(a.strip()) for a in parts[1].split(",")]
            if fname in functions:
                func = functions[fname]
                old_vars = variables.copy()
                for p, a in zip(func["params"], args):
                    variables[p] = a
                run_block(func["body"])
                variables.update(old_vars)
            else:
                print(f"Function '{fname}' not defined")
        elif line.startswith("repeat "):
            parts = line.split(" times do")
            count = int(eval_expr(parts[0][7:]))
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "end":
                block.append(lines[i])
                i += 1
            for _ in range(count):
                run_block(block)
        elif line.startswith("if "):
            cond_line = line[3:].split(" do")[0].strip()
            var, op, val = cond_line.split(" ")
            block = []
            else_block = []
            i += 1
            collecting_else = False
            while i < len(lines) and lines[i].strip() != "end":
                l = lines[i].strip()
                if l == "else":
                    collecting_else = True
                    i += 1
                    continue
                if collecting_else:
                    else_block.append(lines[i])
                else:
                    block.append(lines[i])
                i += 1
            if op == "equals":
                if str(variables.get(var, "")) == val:
                    run_block(block)
                else:
                    run_block(else_block)
        else:
            run_line(line)
        i += 1

def run_line(line):
    line = line.strip()
    if line.startswith("say "):
        print(eval_expr(line[4:]))
    elif line.startswith("ask "):
        parts = line[4:].split(" and set ")
        prompt = eval_expr(parts[0])
        var_name = parts[1].strip()
        variables[var_name] = input(prompt + " ")
    elif line.startswith("set "):
        parts = line[4:].split(" to ")
        var_name = parts[0].strip()
        variables[var_name] = eval_expr(parts[1])
    elif line.startswith("run "):
        fname = line[4:].strip()
        if fname.startswith('"') and fname.endswith('"'):
            fname = fname[1:-1]
        elif fname.startswith("'") and fname.endswith("'"):
            fname = fname[1:-1]
        possible_paths = [
            fname,
            os.path.join(os.getcwd(), fname),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
        ]
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    content = f.read().splitlines()
                run_block(content)
                return
        print(f"File '{fname}' not found")
    elif line.startswith("append "):
        parts = line[7:].split(" with ")
        var_name = parts[0].strip()
        value = eval_expr(parts[1])
        lst = variables.get(var_name, [])
        if not isinstance(lst, list):
            lst = [lst]
        lst.append(value)
        variables[var_name] = lst
    elif line.startswith("remove "):
        parts = line[7:].split(" from ")
        value = eval_expr(parts[0])
        var_name = parts[1].strip()
        lst = variables.get(var_name, [])
        if isinstance(lst, list) and value in lst:
            lst.remove(value)
        variables[var_name] = lst
    elif line.startswith("contains "):
        parts = line[9:].split(" in ")
        value = eval_expr(parts[0])
        var_name = parts[1].strip()
        result = value in variables.get(var_name, [])
        print(result)

# ------------------------------
# REPL
# ------------------------------

print("Graphion REPL. Type 'exit' to quit. Type 'save FILENAME' to save session.")
script_lines = []

while True:
    try:
        line = input(">>> ").strip()
        if line == "exit":
            break
        elif line.startswith("save "):
            fname = line[5:].strip()
            with open(fname + ".gph", "w") as f:
                f.write("\n".join(script_lines))
            print(f"Session saved to {fname}.gph")
            continue
        script_lines.append(line)
        run_block([line])
    except Exception as e:
        print("Error:", e)
