import requests
from bs4 import BeautifulSoup

def lowercase_and_replace_space(string, character):
    return string.lower().replace(" ", character)

def find_substring(string, substring_to_look_after, substring_to_end_search):
    start_index = string.find(substring_to_look_after)
    end_index = string.find(substring_to_end_search, start_index)

    return string[start_index:end_index]

def remove_html_tags(string):
    soup = BeautifulSoup(string, "html.parser")

    return soup.get_text()

def write_markdown(text, directory, mode):
    with open(directory, mode) as file:
        file.write(text)

def request_problem_info(problem_name, submission_id):
    #Get problem info from leetcode api
    url = "https://leetcode.com/graphql"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    cookies = {
        "LEETCODE_SESSION": "",
        "csrftoken": ""
    }

    #graphql query for requesting problem statement, sqlschemas, acceptance rates, difficulty, and solution code
    query = """
        query problemInfo($titleSlug: String!, $submissionId: Int!) {
            question(titleSlug: $titleSlug) {
                content
                mysqlSchemas
                difficulty
                acRate
            },
            submissionDetails(submissionId: $submissionId) {
                code
            }
        }
    """

    #the problem name and submission id for the specific problem requested
    variables = {
        "titleSlug": problem_name,
        "submissionId": submission_id
    }

    #request info from api
    response = requests.post(
        url,
        json = {
            "query": query,
            "variables": variables
        },
        headers = headers,
        cookies = cookies,
        timeout = 10
    )

    return response.json()

def create_md_sql_tables(schemas, content):
    table_substring = "Create table If Not Exists "
    
    #stores list of strings: [table_name, sql_code, description]
    sql_tables = []

    #get sql table names and sql code
    for item in schemas:
        if table_substring in item:
            sql_table_name = find_substring(item, table_substring, "(")
            #need to remove table substring from beginning to get only the table name
            sql_tables.append([sql_table_name.removeprefix(table_substring), item])

    #get descriptions for sql tables
    for index, table in enumerate(sql_tables):
        #get all content for an sql table starting from the table name to before the end of the description of the table
        #if on last table ending_substring is "Write a solution" otherwise it is title of next table
        if index == len(sql_tables) - 1:
            all_table_info = find_substring(content, f"Table: {table[0]}".strip(), "Write a solution")
        else:
            all_table_info = find_substring(content, f"Table: {table[0]}".strip(), f"Table: {sql_tables[index + 1][0]}".strip())
        #get all content starting from the end of leetcode's text table to the end of the description of the table
        #first find last occurence of leetcode's text table formatting
        end_of_leetcode_table_index = all_table_info.rfind(r"-+")
        
        #then find table description exlcuding the beginning of the last occurrence of leetcode's text table formatting; since finding_substring doesn't include ending_substring only need to get the substring starting from end_of_leetcode_table_index to the end of the string
        #remove whitespace and character "+" then add description to list
        table.append(all_table_info[end_of_leetcode_table_index + 1:].strip().replace(r"+", ""))

    #create markdown text with sql tables
    return f"{'\n\n'.join([f'Table: {table[0]}\n\n```sql\n{table[1]}\n```\n{table[2]}' for table in sql_tables])}"

def create_md_problem_statement(content):
    #find the problem statement
    starting_substring = "Write a solution"
    ending_substring = "The result format is in the following example."
    
    return find_substring(content, starting_substring, ending_substring).strip()

def create_md_solution(solution):
    return solution.replace("-- Write your PostgreSQL query statement below", "").strip()
    
def create_markdown_text(problem_name,  data):
    content = remove_html_tags(data["data"]["question"]["content"])
    schemas = data["data"]["question"]["mysqlSchemas"]
    solution = data["data"]["submissionDetails"]["code"] 
    
    problem_statement = create_md_problem_statement(content)
    sql_tables = create_md_sql_tables(schemas, content)
    md_solution = create_md_solution(solution)
    
    return (
        f"## {problem_name.title()}\n\n"
        "### Problem Statement\n\n"
        f"{sql_tables}\n\n"
        f"{problem_statement}\n\n"
        "### Solution\n\n"
        "```sql\n"
        f"{md_solution}\n"
        "```\n\n"
        "### Notes"
    )

def update_readme_file(data, problem_name, problem_num, folder_name):
    difficulty = data["data"]["question"]["difficulty"]
    acceptance_rate = data["data"]["question"]["acRate"]
    directory = "C:/Users/acedi/OneDrive/Documents/Leetcode SQL Questions/README.md"
    markdown_text = (
        f"\n| {problem_num}. | {problem_name.title()} | {difficulty.capitalize()} | {acceptance_rate:.1f}% | {folder_name.title()} |"
    )
    write_markdown(markdown_text, directory, "a")
    

def create_md_file(problem_name, problem_num, folder, submission_id):
    folder_name = lowercase_and_replace_space(folder, "_")

    file_name = problem_num + "_" + lowercase_and_replace_space(problem_name, "_")

    directory = f"C:/Users/acedi/OneDrive/Documents/Leetcode SQL Questions/{folder_name}/{file_name}.md"

    query_problem_title = lowercase_and_replace_space(problem_name, "-")

    data = request_problem_info(query_problem_title, submission_id)
    
    markdown_text = create_markdown_text(problem_name, data)

    #create new markdown file for specific problem
    write_markdown(markdown_text, directory, "w")

    update_readme_file(data, problem_name, problem_num, folder)
        
    print("File successfully created!")
