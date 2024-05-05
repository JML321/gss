The following is broken down into Project Overview and Project Steps (Data Preparation, Website Preparation)

I) Project Overview:

Many [commentators](url) have noted America's substantial shift on abortion over the last two decades. I wanted to find out on which issues America, and certain subcohorts of America, have shifted most on given a certain time period. I wanted this information to be in an interactive table, and make use of the GSS. GSS is one of the most reliable polls in the country. Pollsters are trained, participants are paid for focused participation, and surveys go for over an hour. 

II) Project Steps:

a) Data Preparation

Utilized the GSS [dataset](url) which is formatted as follows: each row as an entire survey with a person, and each column is a question with a code, representing the survey participants response. I cleaned the dataset, using create_tables.py to create 16 datatables, the first for the whole dataset, the other 15 for specific subdemographics e.g. Sex - Male. These data tables are stored in the folder r"..\own_data_objects\melted_tables". Using this table, selecting the years, and compare_years_delta in toolbox.py produces the datatable in the website. 

For the data that appears when hovering over column 1, or that provided the labels seen in column 2, I did the following: copied and pasted two pdfs ([GSS Codebook Index, and GSS Codebook Main Body](url)) into seperate text files, and used regex to create two dictionaries. Those two dictionaries, labels, which provides the question for the label when hovering over column 1, and answers, which replaces the answer code (a number) with the actual answer seen in column 2 (e.g. GRASS, 1.0 is replaced by Should). 

b) Website Presentation

Used Heroku, and Dashtable to create the website. The formatting of the site took a good amount of time, working with GPT. 
