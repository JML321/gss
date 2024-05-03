# give me the import statements i need to run this code
import pandas as pd
import sas7bdat, signal, pyreadstat, pickle, os, re


tooltip_headers = ['Hover over the question code for the full question (GSS data)', 
                   'Hover over the question code for context (GSS data)', 
                   'Column 5 - Column 4, data table sorted by this column', 
                   'Of respondents who answered this question in the year shown in the column header, what % had this answer', 
                   'Of respondents who answered this question in the year shown in the column header, what % had this answer']

# given file_path that has keyword per line, convert to list
def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
    return lines

# filter rows by number of possible answers and what year
def filter_by_answers(df, min_answers=1000):
    # Filter rows where Num_Answers is less than the specified minimum
    df = df[df['Num_Answers'] >= min_answers]
    return df

# filter by unique positive answers
def filter_by_unique_positive_answers(df, max_unique_positives=7):
    # Filter the dataframe to include only positive answers
    positive_answers = df[df['Answer'] > 0]
    unique_positives_count = positive_answers.groupby(['YEAR', 'Question'])['Answer'].nunique().reset_index()
    valid_combinations = unique_positives_count[unique_positives_count['Answer'] <= max_unique_positives]
    df_filtered = pd.merge(df, valid_combinations, on=['YEAR', 'Question'], how='inner')
    df_filtered = df_filtered.drop(columns=[col for col in df_filtered if col.endswith('_y')], errors='ignore')
    df_filtered = df_filtered.rename(columns={'Answer_x': 'Answer'})
    return df_filtered

# get data so question columns just become row with id_vars, then columns, and total answers for question, id_vars
def process_survey_data(df, id_vars, exclude_columns=[], include_columns=[], year=1980, min_answers=800):
    # Filter out excluded columns if specified
    if exclude_columns:
        df = df.drop(columns=exclude_columns, errors='ignore')

    # If include_columns is specified, reduce the dataframe to these columns only, plus id_vars
    if include_columns:
        columns_to_keep = id_vars + include_columns
        df = df[columns_to_keep]

    # Filter by year if the year parameter is set and 'YEAR' is one of the id_vars
    if year is not None and 'YEAR' in id_vars:
        df = df[df['YEAR'] >= year]

    # Melting the dataframe to long format
    d_melted = df.melt(id_vars=id_vars, var_name='Question', value_name='Answer')
    d_melted['Answer'] = pd.to_numeric(d_melted['Answer'], errors='coerce')
    d_melted = d_melted[d_melted['Answer'] > 0]

    # Aggregating data for counting positive answers
    question_answer_count = d_melted.groupby(id_vars + ['Question', 'Answer']).size().reset_index(name='Count')
    question_total = d_melted.groupby(id_vars + ['Question']).size().reset_index(name='Total')
    
    # Aggregating total positive answers per question and year
    num_answers_per_question = d_melted.groupby(id_vars + ['Question'])['Answer'].count().reset_index(name='Num_Answers')

    # Calculating percentages
    merged_data = pd.merge(question_answer_count, question_total, on=id_vars + ['Question'])
    merged_data['Percentage'] = (merged_data['Count'] / merged_data['Total']) * 100

    # Merging to include Num_Answers
    final_table = pd.merge(merged_data, num_answers_per_question, on=id_vars + ['Question'])
    final_table = final_table[id_vars + ['Question', 'Answer', 'Percentage', 'Num_Answers']]

    # using previous methods
    final_table = filter_by_unique_positive_answers(final_table, max_unique_positives=7)
    final_table = filter_by_answers(final_table, min_answers=min_answers) 

    return final_table

def format_percentage_column(df):
    # Check if 'Percentage' column exists in the DataFrame
    if 'Percentage' not in df.columns:
        raise ValueError("The DataFrame does not have a 'Percentage' column.")
    
    # Function to format percentage values
    def format_percentage(value):
        return f"{value / 100:.0%}"
    
    # Convert 'Percentage' column to formatted percentage values
    df['Percentage'] = df['Percentage'].apply(format_percentage)
    
    return df

# Example main DataFrame (df) filtering using the pairings DataFrame
def filter_dataframe(main_df, filter_df):
    # Merge main DataFrame with the filter DataFrame to get only the matched rows
    filtered_df = pd.merge(main_df, filter_df, how='inner', on=['YEAR', 'Question'])
    return filtered_df

def compare_years_delta(df, year1, year2):

    # Convert 'YEAR' to float if it's not already
    df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')

    # Filter data for the two years
    df_year1 = df[df['YEAR'] == year1].copy()
    df_year2 = df[df['YEAR'] == year2].copy()

    if df_year1.empty or df_year2.empty:
        raise ValueError("One of the years specified does not contain any data.")

    # Ensure the percentage columns are floats and modify data directly using .loc
    df_year1.loc[:, 'Percentage'] = pd.to_numeric(df_year1['Percentage'], errors='coerce')
    df_year2.loc[:, 'Percentage'] = pd.to_numeric(df_year2['Percentage'], errors='coerce')

    # Rename columns for clarity after merge
    df_year1.rename(columns={'Percentage': f'{year1} Percentage'}, inplace=True)
    df_year2.rename(columns={'Percentage': f'{year2} Percentage'}, inplace=True)

    # Merge the two years' data based on Question and Answer
    merged_df = pd.merge(df_year1[['Question', 'Answer', f'{year1} Percentage']],
                         df_year2[['Question', 'Answer', f'{year2} Percentage']],
                         on=['Question', 'Answer'],
                         how='inner')

    if merged_df.empty:
        raise ValueError("No common Question and Answer pairs found between the two years.")

    # Calculate the delta in percentages
    col_name = f'Change from {year1} to {year2}'
    merged_df[col_name] = merged_df[f'{year2} Percentage'] - merged_df[f'{year1} Percentage']

    # Sort by delta to get the highest changes at the top
    result_df = merged_df.sort_values(by=col_name, ascending=False)

    # # swap third and fifth columns
    cols = result_df.columns.tolist()
    cols[2], cols[3], cols[4] = cols[4], cols[2], cols[3]  # Directly swap the third and fifth columns
    result_df = result_df[cols]
    df = result_df
    df = df.astype(str)
    df.iloc[:, 2] = df.iloc[:, 2].apply(lambda x: f"+{float(x):.1f}%" if float(x) > 0 else f"{float(x):.1f}%")
    df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: f"{float(x):.1f}%")
    df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: f"{float(x):.1f}%")

    return df



def modify_answers(df, answers):
    # Check if the expected columns are present
    if 'Question' not in df.columns or 'Answer' not in df.columns:
        raise ValueError("DataFrame must contain 'Question' and 'Answer' columns")

    # Ensure the Answer column is treated as a string for consistent key comparison
    df['Answer'] = df['Answer'].apply(lambda x: str(int(float(x))).strip() if pd.notna(x) else x)

    # Using apply to process each row; referencing columns by names
    def get_answer(row):
        question = row['Question']
        answer = row['Answer']
        if question in answers and answer in answers[question]:
            return answers[question][answer]
        return answer

    df['Answer'] = df.apply(get_answer, axis=1)
    return df


# for getting first iteration labels and answers
def parse_codebook(file_path):
    # Regular expressions to capture required parts
    variable_pattern = re.compile(r'Variable:\s+(\S+)\s+Type:', re.IGNORECASE)
    label_pattern = re.compile(r'Label:\s*(.*?)(?=Notes:)', re.IGNORECASE | re.DOTALL)
    answer_pattern = re.compile(r'PCT Excl\.\s*Reserve\s*Codes\s*((?:\n(?!\s*TOTAL).+)+)', re.IGNORECASE)

    # Dictionaries to hold the results
    labels_dict = {}
    answer_keys_dict = {}

    # Read and preprocess the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Remove any lines containing "Page"
    content = re.sub(r'^.*Page.*$\n?', '', content, flags=re.MULTILINE | re.IGNORECASE)

    # Split content into sections based on variables
    sections = re.split(r'\n(?=Variable:)', content, flags=re.IGNORECASE)
    previous_label = ""
    previous_variable = ""

    for section in sections:
        # Search for the variable name
        variable_match = variable_pattern.search(section)
        if variable_match:
            variable = variable_match.group(1)

            # Search for the label and clean it
            label_match = label_pattern.search(section)
            if label_match:
                label = label_match.group(1).strip()
                label = re.sub(r'\s*\n\s*', ' ', label)  # Replace newlines with a single space

                # Check if previous and current variable share starting letters
                if previous_variable[:2] == variable[:2]:
                    if '(' in previous_label and '(' not in label:
                        start_index = previous_label.find('(')
                        end_index = previous_label.rfind(')') + 1
                        contextual_part = previous_label[start_index:end_index]
                        label = contextual_part + ' ' + label

                labels_dict[variable] = label
                previous_label = label  # Update previous label
                previous_variable = variable  # Update previous variable

            # Search for the answer keys
            answer_match = answer_pattern.search(section)
            if answer_match:
                answer_text = answer_match.group(1).strip()
                answer_lines = answer_text.split('\n')
                answer_dict = {}
                for line in answer_lines:
                    if 'TOTAL' in line:
                        break
                    # Extract the key and value
                    match = re.match(r"([^\d]+)(\d+)", line)
                    if match:
                        value = match.group(1).strip()
                        key = match.group(2).strip()
                        answer_dict[key] = value

                if answer_dict:
                    answer_keys_dict[variable] = answer_dict

    # Save dictionaries
    directory_path = r"C:\Users\justi\Dropbox\Work\Job Search\Other\GSS\own_data_objects"
    labels_file_path = os.path.join(directory_path, 'labels.pkl')
    answers_file_path = os.path.join(directory_path, 'answers.pkl')

    with open(labels_file_path, 'wb') as file:
        pickle.dump(labels_dict, file)

    with open(answers_file_path, 'wb') as file:
        pickle.dump(answer_keys_dict, file)

    return labels_dict, answer_keys_dict

def parse3(variable):
    whole_filepath = '../own_data_objects/GSS2022_whole.txt'  # Path to the whole data file
    variable_tag = f'[VAR: {variable}]'  # Format the variable tag to look for

    with open(whole_filepath, 'r', encoding='utf-8') as file:  # Open the file with UTF-8 encoding
        capture = False  # Flag to start capturing data after finding the variable
        after_all = False  # Flag to start recording after "ALL"
        answers = {}  # Dictionary to store the response codes and their descriptions
        
        for line in file:
            line = line.strip()  # Strip any leading/trailing whitespace
            
            if after_all:
                if 'Not applicable' in line:  # Stop capturing on this line
                    break
                # Split the line to separate the description from the codes
                import re
                match = re.split(r'(\d+)', line, 1)  # Split by the first number
                if len(match) >= 2:
                    description = match[0].strip()
                    code = match[1].strip()
                    answers[code] = description
                    # debugging
                    # print(f"Captured: {code} -> {description}")  # Debug output
                else:
                    # debugging
                    # print(f"Skipping line: {line}")  # Debug output for non-data lines
                    pass

            if capture and "ALL" in line:  # This marks the start of the actual data capture
                after_all = True

            if variable_tag in line:  # Check for the specific variable line
                # print(f"Found variable line: {line}")  # Debug output
                capture = True  # Set capture flag to true to start capturing data

    # print("Final captured answers:", answers)  # Output final dictionary
    return answers  # Return the dictionary of response codes and descriptions

def parse2(label):
    index_filepath = '../own_data_objects/GSS_index.txt'  # Path to the index file
    with open(index_filepath, 'r') as file:  # Open the file in read mode
        for line in file:  # Iterate over each line in the file
            if line.startswith(label + " "):  # Check if the line starts with the label followed by a space
                return line.strip().split(' ', 1)[1]  # Split the line at the first space and return the description part
    return None  # Return None if label is not found

def unpickle(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return data