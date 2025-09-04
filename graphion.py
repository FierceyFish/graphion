# Graphion v1.4.1 Interpreter

import random
import time
import os

variables = {}
history = []

def current_time():
    return time.strftime("%H:%M:%S")

def get_value(token):
    token = token.strip()
    if token in variables:
        return variables[token]
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return token

def eval_expr(expr):
    expr = expr.strip()
    if expr.startswith("round "):
        return round(float(get_value(expr[6:])))
    if expr.startswith("length "):
        val = get_value(expr[7:])
        if isinstance(val, (str, list)):
            return len(val)
        return 0
    if expr.startswith("uppercase "):
        return str(get_value(expr[10:])).upper()
    if expr.startswith("current_time"):
        return current_time()
    if expr.startswith("random "):
        parts = expr.split()
        return random.randint(int(parts[1]), int(parts[2]))
    if " + " in expr:
        left, right = expr.split(" + ", 1)
        return str(get_value(left)) + str(get_value(right))
    return get_value(expr)

def run_block(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        # single-line if/else support
        if line.startswith("if "):
            if " do" in line or line.endswith("end"):
                # multi-line if: handled below
                pass
            else:
                # single-line if or if-else
                cond_part = line[3:]
                if " else " in cond_part:
                    cond_expr, cmd = cond_part.split(" else ", 1)
                    var, _, val = cond_expr.partition(" equals ")
                    if str(variables.get(var.strip(), "")) == val.strip():
                        run_block([cmd.strip()])
                    else:
                        run_block([cmd.strip()])
                else:
                    var, _, val_cmd = cond_part.partition(" equals ")
                    val, _, cmd = val_cmd.partition(" ")
                    if str(variables.get(var.strip(), "")) == val.strip():
                        run_block([cmd.strip()])
                i += 1
                continue

        parts = line.split(" to ", 1)
        if line.startswith("set "):
            var = line[4:].split(" to ")[0].strip()
            val_expr = line[4+len(var)+4:].strip()
            variables[var] = eval_expr(val_expr)
        elif line.startswith("say "):
            print(eval_expr(line[4:]))
        elif line.startswith("ask "):
            if " and set " in line:
                prompt, var = line[4:].split(" and set ", 1)
                variables[var.strip()] = input(prompt.strip() + " ")
        elif line.startswith("repeat "):
            count = int(eval_expr(line[7:].split(" times")[0]))
            sub_lines = []
            i += 1
            depth = 1
            while i < len(lines) and depth > 0:
                sub_line = lines[i].strip()
                if sub_line == "end":
                    depth -= 1
                elif sub_line.startswith("repeat "):
                    depth += 1
                if depth > 0:
                    sub_lines.append(sub_line)
                i += 1
            for _ in range(count):
                run_block(sub_lines)
            continue
        elif line.startswith("if "):
            if " do" in line:
                cond_expr = line[3:].split(" do")[0].strip()
                var, _, val = cond_expr.partition(" equals ")
                sub_lines = []
                i += 1
                depth = 1
                while i < len(lines) and depth > 0:
                    sub_line = lines[i].strip()
                    if sub_line == "end":
                        depth -= 1
                    elif sub_line.startswith("if "):
                        depth += 1
                    if depth > 0:
                        sub_lines.append(sub_line)
                    i += 1
                if str(variables.get(var.strip(), "")) == val.strip():
                    run_block(sub_lines)
                continue
        elif line.startswith("run "):
            fname = eval_expr(line[4:])
            if os.path.exists(fname):
                with open(fname, "r") as f:
                    run_block(f.readlines())
            else:
                print(f"File '{fname}' not found")
        elif line.startswith("save "):
            fname = line[5:].strip()
            with open(fname + ".gph", "w") as f:
                f.write("\n".join(history))
        else:
            # attempt expression evaluation
            eval_expr(line)
        history.append(line)
        i += 1

def repl():
    print("Graphion REPL v1.4.1. Type 'exit' to quit. Type 'save FILENAME' to save session.")
    while True:
        try:
            line = input(">>> ").strip()
        except EOFError:
            break
        if line.lower() == "exit":
            break
        if line:
            run_block([line])

if __name__ == "__main__":
    repl()
