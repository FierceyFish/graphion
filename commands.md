**Graphion Commands Cheat Sheet**
*Core Commands*

say – Print text or variables

say "Hello, world!"
say "Your name is " + name


ask – Prompt input from the user

ask "Enter your name:" and set name


set – Assign value to a variable

set task_count to 5
set tasks to ""
set tasks to join tasks with ", " + new_task


repeat – Loop commands N times

repeat 3 times do
    say "Hello"
end


if / else – Conditional execution (multi-line & single-line)

if tasks equals "" do
    set tasks to task_input
else
    set tasks to join tasks with ", " + task_input
end

# Single-line example
if name equals "user" say "Hi" else say "Hello"


join – Join strings with a separator

set tasks to join tasks with ", " + new_task


split – Split a string into a list

set task_list to split tasks by ", "


random – Generate a random integer in a range

set i to random 1 1000
set random_index to random 0 length task_list - 1


length – Get the length of a string or list

set n to length task_list


uppercase – Convert text to uppercase

say "Hello " + uppercase name


round – Round a number to the nearest integer

set task_count to round task_count


current_time – Get the current system time as a string

say current_time


run – Run a .gph script file from REPL

run example_script.gph


save – Save the current REPL session to a file

save mysession

Example Quick Reference

Greeting the user

ask "What is your name?" and set name
say "Hello " + uppercase name + "!"


Daily tasks input

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


Random motivational message

set messages to "Stay focused,Keep it up,You can do it,Make today great,Keep pushing"
set msg_list to split messages by ","
set rand_index to random 0 length msg_list - 1
say "Motivation: " + msg_list[rand_index]
