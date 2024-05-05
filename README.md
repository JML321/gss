The following summary of this github project is broken down into two parts: Project Overview and Project Steps (Data Preparation, Website Preparation)

I) Project Overview:

Many [commentators](url) have observed significant shifts in America's views on issues such as abortion over the last two decades. This project aims to explore broader trends by identifying which issues have seen the most significant changes in public opinion. An interactive website has been developed to showcase these changes, allowing users to select different demographics and time periods for analysis. The data, sourced from the General Social Survey (GSS), benefits from rigorous collection methods: trained pollsters, compensated participants, in-person surveys, and sessions lasting over an hour, ensuring reliability and depth.

II) Project Steps:

a) Data Preparation

The foundation of this project is the GSS [dataset](url) where each row corresponds to a complete survey conducted with an individual, and each column represents a response or a demographic attribute. Initial data cleaning involved removing questions with low response rates or that were unrelated to beliefs (e.g. BALLOT, ballot type used in the interview). Subsequently, 16 data tables were created—one representing the entire population and the others for specific demographic groups like males and young people. These tables are stored in "..\own_data_objects\melted_tables". A crucial function, compare_years_delta in toolbox.py, is used to generate the datatable seen on the website, using one of the melted tables, start year, and final year. This datatable is then sorted to highlight which issues have experienced the most substantial shifts in public opinion.

For the tooltips in column 1, or the values in column 2, I did the following: copied and pasted two pdfs ([GSS Codebook Index, and GSS Codebook Main Body](url)) into seperate text files, and used regex to create two dictionaries called labels and answers. “labels” provides the question for the label when hovering over column 1, and “answers”, which replaces the answer code (a number) with the actual answer seen in column 2 (e.g. GRASS, 1.0 is replaced by Should).

b) Website Presentation

Heroku was used for the hosting for the website, and Dashtable to create the datatable/ layout of the site. 
