# Parse Oracle Trace File
Recently, the customer always complained that the process became slow. So we plan to do it step by step to try to find which step causes the performance down.
But when we execute the plan, we find every step looks like normal, there is no step to let us feel exception.

I think that perhaps it is not a special step cause the issue. because the logic of program has a big loop, 
the count of the loop that program executes is about 1000, if there are 500 operations in a loop, all work of the task will have 500000 operations.

if we suppose a step delay average 0.0001 seconds which contrast to the normal situation, all tasks will delay 500 seconds, about 10 minutes.

But it is difficult to trace every operation in the program. In general, we can write a log in the program to record the time of consumption of the operation.
but it's impossible to add a log for all operations in the program. we need a more efficient way.

Fortunately, we know that Oracle can trace the session, which will record all SQL statements that the session executed and output to a trace file binding with the session.
but it's raw data whose means of every data is obscure. it needs to be converted to be human-readable.

So we have the initial code, but it has a lot of issues. at least, we can analyze the data in the trace file, return the time consumption of every SQL statements. 

I hope everyone who is interested in can help me improve it. 
Thanks a lot.
