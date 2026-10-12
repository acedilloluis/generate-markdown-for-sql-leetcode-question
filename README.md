## Create a Markdown File for Each Question in the SQL-LeetCode-Questions Repository and Update Its README

### Description

A Python script for creating a markdown file containing the problem statement and my solution for a specific SQL LeetCode question and for updating the README file of the SQL-LeetCode-Questions repository. The script takes 4 inputs: the name of the problem, the number of the problem, the folder name the markdown file should be saved in, and the submission id for the particular solution to be included in the markdown file. The script then queries LeetCode's GraphQL API endpoint to get the problem statement and my submitted solution. It then cleans this data by removing any HTML tags and transforms this data into the desired markdown format. It then adds the problem to the table of contents in the README file of the SQL-LeetCode-Questions repository.

### Reason for Writing Script

To automate the process of creating a markdown file for a backlog of solved SQL LeetCode questions and of creating a markdown file for solved problems in the future. 

