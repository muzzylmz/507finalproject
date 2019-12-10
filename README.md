# 507finalproject

Project Proposal 

Data source: 
Since I want to be a UX researcher/ designer in the future, my eyes are always open on the job site for UX positions. Therefore, I used this website: https://www.uxjobsboard.com/. I went through each subpage of job posting to crawl and scrape all the variables I wanted, such as job title, company name, job postdate. 

Code structure: 
I created two tables: companies and jobs in SQL database. The jobs table has the following variables: id, title, jobtype, companyname, companyid, and postdate. The companies table has id, name, city, country, lat, lon, companysite. 
I had two classes: ux_company_list and ux_jobs_list. Both functions will return a string statement. 
There are four graphs/diagrams to illustrate the relationship between these variables.  

User guide: 
To begin with, run the file in command. Following the instruction- input “help”, “plots”, “list”, and “exit”, for other inputs, it will return “command not recognized”. For “help”, it will give an instruction to guide what plots are available to display. 
 
In order to process to navigate to plots, please enter “Help” first. 
You will see a visualization menu, with options are “exit”, “1”, “2”, “3”, “4”, “all”, otherwise “Error. Invalid command”. The numbers correspond to each plot. Pick a plot and type the number. The plot will show up. 
