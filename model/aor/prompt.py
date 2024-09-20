from IPython.core.debugger import prompt

question_prompt = "This is the question: "

local_evaluation = """Evaluate the solution process for the problem using the criteria below, with a 
maximum score of 10 points:
• Logical Consistency (3 points)
• Appropriateness of Method (3 points)
• Completeness and Clarity (2 points)
• Application of Knowledge (2 points)
the score should be putted in the last line of the answer in a int format.
"""
global_evaluation = """"Multiple solution processes are presented below, each leading to a different answer. 
Only one of these answers is correct. Evaluate each solution process based on:
 • Validity of Approach (3 points)
 • Consistency of Steps and Answer (3 points)
 • Completeness and Clarity (2 points)
 • Application of Knowledge (2 points)
 the score should be putted in the last line of the answer in a int format.
 """

prompt_before_answer = "this is one of the solution process to be evaluated:"

answer_number_last = "please repeat the final answer at the end of the answer in  a   int or float format   ."
cot_prompt = """let's think step by step:"""