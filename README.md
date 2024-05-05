The following summary of this github project is broken down into two parts: Project Overview and Project Steps (Data Preparation, Website Preparation)

I) Project Overview:

Many [commentators](url) have noted America's substantial changing view on abortion over the last two decades. I wanted to know on what other issues has America shifted on, and by how much. This project creates an interactive website that shows which issues America has moved the most on, selecting for Demographic and Timeline. The data used to generate the table comes from the GSS. GSS is one of the most reliable polls in the country. Pollsters are trained, participants are paid, surveys are in person, and typically go over an hour. 

II) Project Steps:

a) Data Preparation

All the data comes from the GSS [dataset](url) where each row represents a full survey with an individual, and each column is an attribute about the interview such as the response to a question or characteristic of the individual. First the dataset was cleaned, doing steps such as removing questions with a low number of responses or questions not related to a belief (e.g. BALLOT, which ballot was used for the interview). Next, 16 datatables were created, one for the whole population, and the rest for specific demographic groups e.g. Males, young people. These data tables are stored in the folder r"..\own_data_objects\melted_tables". Passing a table in "melted_tables", along with a start year and an end year, as parameters to the compare_years_delta function in toolbox.py generates a datatable that is displayed on the website

For the data that appears when hovering over column 1, or that are the values in column 2, I did the following: copied and pasted two pdfs ([GSS Codebook Index, and GSS Codebook Main Body](url)) into seperate text files, and used regex to create two dictionaries called labels and answers. “labels” provides the question for the label when hovering over column 1, and “answers”, which replaces the answer code (a number) with the actual answer seen in column 2 (e.g. GRASS, 1.0 is replaced by Should).

b) Website Presentation

Used Heroku as the server for the website, and Dashtable to create the datatable/ layout of the site. 
