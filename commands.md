# Graphion Commands Cheat Sheet & Examples

## Commands

**say** – Print text or variables: `say "Hello, world!"`  
**ask** – Prompt input: `ask "Enter name:" and set name`  
**set** – Assign value: `set task_count to 5`, `set tasks to ""`  
**repeat** – Loop N times: `repeat 3 times do ... end`  
**if / else** – Conditional: `if tasks equals "" do ... else ... end`  
**join** – Join strings: `set tasks to join tasks with ", " + new_task`  
**split** – Split string: `set task_list to split tasks by ", "`  
**random** – Random number: `set i to random 1 1000`  
**length** – Get length: `set n to length task_list`  
**uppercase** – Uppercase text: `say "Hello " + uppercase name`  
**round** – Round number: `set task_count to round task_count`  
**run** – Run script file: `run example_script.gph`  
**save** – Save REPL session: `save mysession`

## Quick Examples

**Example 1 – Greeting user**  


ask "What is your name?" and set name
say "Hello " + uppercase name + "!"


**Example 2 – Daily tasks loop**  


ask "How many tasks today?" and set task_count
repeat task_count times do
ask "Enter task:" and set task
if tasks equals "" do
set tasks to task
else
set tasks to join tasks with ", " + task
end
end
say "Your tasks: " + tasks


**Example 3 – Random motivational message**  


set messages to "Stay focused,Keep it up,You can do it,Make today great,Keep pushing"
set msg_list to split messages by ","
set rand_index to random 0 length msg_list - 1
say "Motivation: " + msg_list[rand_index
