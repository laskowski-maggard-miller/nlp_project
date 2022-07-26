## PREDICTING PRIMARY GITHUB REPOSITORY LANGUAGE BASED ON README TEXT

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Project Summary
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

#### Project Objectives
> - Can we determine the primary coding language used for a github repository only using the text within the repo's Readme? This then begs the more general question: if we have a bunch of text describing a coding project, can we determine which language is being used without explictly being told?

#### Goals
> - Identify Key Characteristics of github readmes that signal the dominant language used in the repository.
> - Sufficiently scrape and clean information from the internet (github) in such a way that NLP techniques and analysis can be used.
> - Construct a ML classification model that predicts what the primary language of a given repo is based on the readme (size, structure and words used).
> - Document my process well enough to be presented or read like a report.

#### Audience
> - Github Fanatics
> - Cat conspiracy nutjobs
> - CodeUp Students!

#### Project Deliverables
> - A final report notebook (Repo_Analysis_Final.ipynb)
> - A short presentation with our results and recommendations for the future
> - All relevant helper functions to duplicate this project.
> - All necessary modules to make my project reproducible

#### Data Dictionary
- Note: Includes only those features selected for full EDA and Modeling:

|Target|Datatype|Definition|
|:-------|:--------|:----------|
| language_group | 743 non-null: object | Primary language of the repo code (Python, Scala JavaScript or Other) |

|Feature|Datatype|Definition|
|:-------|:--------|:----------|
| language       | 743 non-null: object | Primary language of repo |
| readme_contents        | 743 non-null: object | Raw string from acquire function |
| cleaned        | 743 non-null: object | Cleaned and prepared string for analysis |
| cleaned_length        | 743 non-null: object | Word count of cleaned string |


#### Initial Hypotheses

> - **Hypothesis 1 -**
> - There is a difference in cleaned repo word count between different langauges' readmes.

> - **Hypothesis 2 -** 
> - There are key words and bigrams in readmes that are indicative of the primary language used in the code. 

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Executive Summary + Conclusions & Next Steps
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

> - Question: Can we determine the primary coding language used for a github repository only using the text within the repo's Readme?  This then begs the more general question: if we have a bunch of text describing a coding project, can we determine which language is being used without explictly being told?
> - Actions: In order to find a repo set that was cross-cutting enough to get a broad sample of project types and languages, we did an analysis of the top 1000 repos - sorted by best match - that came up when searching for the term 'cats'.  We used text parsing tools to scrape the Readme's of these repos, as well as the primary language as determined by Github.  We performed cleaning operations on the text to optimize it for analysis and modeling using NLP techniques.  Lastly, we sought to determine key signals of repo language, as well as build a classification model to accurately predict the language on out-of-sample repos.
> - Conclusions:  There are certain words and bigrams that are indicative of primary programming language.  The actual length of the readme isn't nearly as predictive as these words.  In addition, modeling using TF-IDF greatly improves upon the baseline accuracy of determining the language based on readme text alone of out-of-sample data (65% vs 47.5%)
> - Recommendations: We feel the model can be tuned for an even greater accuracy.  Once accuracy is dialed in, we can include more than just the primary language of the repo for greater granularity!

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Pipeline Stages Breakdown

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

##### Plan
- [x] Create README.md with data dictionary, project objectives and goals, come up with initial hypotheses.
- [x] Acquire data from Github and create a function to automate this process. Save the function in an acquire.py file to import into the final Notebook. Also, cache locally, since that is always good practice.
- [x] Clean and prepare data for the first iteration through the pipeline: MVP preparation. Create a function to automate the process, store the function in a wrangle.py module, and prepare data in final Study Notebook by importing and using the function.
- [x] Investigate data, formulate hypotheses, visualize analsyis and run statistical tests when necessary (ensuring signifigance and hypotheses are created and usability assumptions met).  Document findings and takeaways.
- [x] Use NLP and TF-IDF to better understand the data and create new features.
- [x] Establish a baseline modeling accuracy.
- [x] Train multiple different classicitcation models, to include hyperparameter tuning.
- [x] Evaluate models on train and validate datasets.
- [x] Choose the model with that performs the best and evaluate that single model on the test dataset.
- [x] Document conclusions, takeaways, and next steps in the final Notebook.

___

##### Plan -> Acquire
> - Store functions that are needed to acquire data from the database server; make sure the acquire.py module contains the necessary imports for anyone with database access to run the code.
> - The final function will return a pandas DataFrame.
> - Import the acquire function from the acquire.py module and use it to acquire the data in the final Study Notebook.
> - Complete some initial data summarization (`.info()`, `.describe()`, `.value_counts()`, etc.).
> - Plot distributions of individual variables.
___

##### Plan -> Acquire -> Prepare/Wrange
> - Store functions needed to wrangle the data; make sure the module contains the necessary imports to run the code. The final functions (wrangle.py) should do the following:
    - Split the data into train/validate/test.
    - Handle any missing values.
    - Handle erroneous data and/or outliers that need addressing.
    - Encode variables as needed.
    - Create any new features, if made for this project.
> - Import the prepare functions from the wrangle.py module and use it to prepare the data in the final Notebook.
___

##### Plan -> Acquire -> Prepare -> Explore
> - Answer key questions, my hypotheses, and figure out the features that can be used in a classification model to best predict the target variable, has Earthlike planet (or not). 
> - Run at least one statistical tests in data exploration. Document my hypotheses, set an alpha before running the tests, and document the findings well.
> - Create visualizations and run statistical tests that work toward discovering variable relationships (independent with independent and independent with dependent). The goal is to identify features that are related to language group (the target), identify any data integrity issues, and understand 'how the data works'. If there appears to be some sort of interaction or correlation, assume there is no causal relationship and brainstorm (and document) ideas on reasons there could be correlation.
> - Summarize my conclusions, provide clear answers to my specific questions, and summarize any takeaways/action plan from the work above.
___

##### Plan -> Acquire -> Prepare -> Explore -> Model
> - Feature Selection and Encoding: Are there any variables that seem to provide limited to no additional information? If so, remove them.  Also encode any non-numerical features of signifigance.
> - Establish a baseline accuracy to determine if having a model is better than no model and train and compare at least 4 different models.
> - Train (fit, transform, evaluate) multiple models, varying the algorithm and/or hyperparameters you use.
> - Compare evaluation metrics across all the models you train and select the ones you want to evaluate using your validate dataframe.  In this case we used Precision (Positive Predictive Value).
> - Based on the evaluation of the models using the train and validate datasets, choose the best model to try with the test data, once.
> - Test the final model on the out-of-sample data (the testing dataset), summarize the performance, interpret and document the results.
___

##### Plan -> Acquire -> Prepare -> Explore -> Model -> Deliver
> - Summarize our findings at the beginning like we would for an Executive Summary.
> - Walk the management team through the analysis I did to answer my questions and that lead to my findings. (Visualize relationships and Document takeaways.) 
> - Clearly call out the questions and answers I am analyzing as well as offer insights and recommendations based on my findings.

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Reproduce Our Project

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

You will need all the necessary files listed below to run my final project notebook. 
- [x] Read this README.md
- [ ] Download the aquire.py, prepare.py, wrangle.py, and explore.py files into your working directory.
- [ ] To save yourself time and frustration, download the repo_list.csv to use with the acqurie function, or skip ahead and download the cached data.json file
- [ ] For more details on the analysis, in particular clustering charts, download the subsection workbooks.
- [ ] Run the Repo_Analysis_Final.ipynb notebook

##### Credit to Faith Kane (https://github.com/faithkane3) for the format of this README.md file.