"""
Quinn Nguyen
524002419
CSCE 315-503
Due: September 10, 2018
README.TXT
"""
Description of Program:
query_server_list(serverList) takes an array of servers as an argument and query each server. This function will query every server first and record the difference.  If a server times out, the difference will be 5.
Then, it will calculate the sum(excluding difference of 5) to compute approriate discrepancy. I store each server and its discrepancy value in a dictionary. During this calculation, I also keep track the greatest discrepancy.
At the end, the result of server name with greatest discrepancy will be displayed on the screen. Then, a bar graph will be displayed.  Please note that any click on the graph will cause the bar graph to exit.

Instruction:
1) Call function query_server_list(serverList) and pass an array of servers to the argument.
2) Wait and see the result appear on the screen with print statement.
3) The bar graph will follow short after. 
Note: if you want to disable graph, please comment out "draw_graph(serverDict)" at the end of query_server_list function or line 77


