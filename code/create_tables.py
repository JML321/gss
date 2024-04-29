import pandas as pd
import sas7bdat, signal, pyreadstat, pickle
from toolbox import *

############# vars so can find correct melted table for the website #############
place = {"AGE":1, "DEGREE":5, "PARTYID":8,"SEX":11,"RACE":13}
# 5 each row
naming = ["The Country", "18-34", "35-49", "50-64", "65+", 
          "No High School", "High School", "College+", "Democrat", "Independent/ Other", 
          "Republican", "Male", "Female", "White", "Black", 
          "Other"]

data_path = r"C:\Users\justi\Dropbox\Work\Job Search\Other\GSS\GSS_sas\gss7222_r3.sas7bdat"
df, meta = pyreadstat.read_sas7bdat(data_path)

############# cleaning df #############
# df is the original data - each column header is a question, each row is respondents answers
# need to change the values in the Age column to 0 if between 18-34
# 1 if between 35-49, 2 if between 50-64, 3 if 65+
df['AGE'] = df['AGE'].apply(lambda x: 0 if x < 35 else 1 if x < 50 else 2 if x < 65 else 3)
# do same for degree, where is 3 or 4, make it 2
df['DEGREE'] = df['DEGREE'].apply(lambda x: 2 if x >= 2 else x)
# for partyid, if 0-1 do 0, 2-4,7 do 1, 5-6 do 2
df['PARTYID'] = df['PARTYID'].apply(lambda x: 0 if x < 2 else 1 if x < 5 or x == 7 else 2)
# leaving sex and race alone, those go from 1-2 and 1-3 respectively

############# creating df_list #############
df_list = [df] # 0
age_list = [df[df['AGE'] == age] for age in range(4)] # 1-4
degree_list = [df[df['DEGREE'] == degree] for degree in range(3)] # 5-7
partyid_list = [df[df['PARTYID'] == partyid] for partyid in range(3)] # 8-10
sex_list = [df[df['SEX'] == sex] for sex in range(1, 3)] # 11-12
race_list = [df[df['RACE'] == race] for race in range(1, 4)] # 13-15
df_list.extend(age_list)
df_list.extend(degree_list)
df_list.extend(partyid_list)
df_list.extend(sex_list)
df_list.extend(race_list)

print("main df is size: ", df_list[0].shape)
for i in range(11, 13):
    print("one part of sex df is size: ", df_list[i].shape)
for i in range(8, 11):
    print("one part of partyid df is size: ", df_list[i].shape)

############# params for creating first melted table #############
# df, id_vars, exclude_columns, include_columns, year, min_answers
paradata_keywords = read_file_lines(r"C:\Users\justi\Dropbox\Work\Job Search\Other\GSS\GSS_sas\Paradata_variables.txt")
df = df; id_vars=['YEAR']; exclude_columns=['ID']+(paradata_keywords); include_columns=[]
year = 2000; min_answers = 850

############# creating first melted table, and params to filter future ones #############
# melted table cols --- id_vars (YEAR), Question, Answer, Percentage, Num_Answers
melted_list = []
melted_list.append(process_survey_data(df, id_vars=id_vars, exclude_columns=exclude_columns, include_columns=include_columns, year=year,min_answers=min_answers))
filter_df = melted_list[0][["YEAR", "Question"]].drop_duplicates()

print("past first table")

############# creating future melted tables #############
for i in range(1, len(df_list)):
    df = df_list[i]
    # min_answers = 0 because already got YEAR, Question pairings of interest from first df
    melted_df = process_survey_data(df, id_vars=id_vars, 
        exclude_columns=exclude_columns, include_columns=include_columns, 
        year=year, min_answers=0)
    filtered_df = filter_dataframe(melted_df, filter_df)
    melted_list.append(filtered_df)

print("past other tables")
for i in range(1, len(melted_list)):
    print("one melted table is size: ", i, " ",melted_list[i].shape)

############# saving melted tables #############

output_folder = r"..\own_data_objects\melted_tables"
for i, df in enumerate(melted_list, 0):
    output_path = os.path.join(output_folder, f'melted_table_{i}.csv')
    df.to_csv(output_path, index=False)  # index=False if you do not want the row indices saved in the file

            
############# testing melted tables #############
# # main
# main_melted = melted_list[0]
# print("testing main list")
# print(main_melted.head(10))

# print("seeing final table for main")
# final_table = compare_years_delta(main_melted, 2008, 2018)
# print(final_table.head(50))

# # young
# young_melted = melted_list[1]
# print("testing young list")
# print(young_melted.head(10))

# print("seeing final table for young")
# final_table = compare_years_delta(young_melted, 2008, 2018)
# print(final_table.head(50))


# # male
# male_melted = melted_list[11]
# print("testing male list")
# print(male_melted.head(10))

# print("seeing final table for male")
# final_table = compare_years_delta(male_melted, 2008, 2018)
# print(final_table.head(50))

# # female
# female_melted = melted_list[12]
# print("testing female list")
# print(female_melted.head(10))

# print("seeing final table for male")
# final_table = compare_years_delta(female_melted, 2008, 2018)
# print(final_table.head(50))

############# saving melted tables #############

