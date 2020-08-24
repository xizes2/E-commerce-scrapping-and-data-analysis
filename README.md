# Python Web Scraping + Jupyter Data Analysis

**Primarily objective:**

See the price variation on an number of products. Check what´s the store policy for the black friday discount day (previous and actual day).
 
**1st step - Python:**

The python application has two scripts, one for the first time the user is running this project and a second one for everytime after that.
 
 * The first script fetches the information on the selected sites and create an excel to save the information. After the first use of the first script, the second script will be the only one used if the user wants to keep the results on the same excel file.
 
 * The second script will access the pre-selected web pages, fetch the pre-determined information, print it on the screen and save it to the existing excel file (created before with the first use of the first script) on a different tab with the date as the name of that tab.
 
**2nd step - Jupyter:**

We´ll use the excel file created previously to organize, treat and clean the information so we can print the graphics and see the prices variation.

*Issue to be solved: Deal with the days where there´s no information about any given product. Fill those days with 'nan' so the whole dataframe has all the cells fulfilled*
