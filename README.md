# Semantic-Legal-Information-Systems

LII must combine its mined entity text-data from diverse sources to build its ontologies, yet it has no automated model in place yet to verify the relationships between such texts as to confidently join the data.
Thus, this project developed a scalable, unsupervised exploratory prototype for this sort of automated legal information retrieval and extraction. 

# Prerequisite Libraries

We need sklearn, pandas, gensim, sentence_transformers, and requests. Python should already include all other libraries used such as json, time, and csv.
The following terminal commands should install each library, respectively:

  pip install -U scikit-learn
  
  pip install pandas
  
  pip install -U gensim
  
  pip install -U sentence-transformers
  
  pipenv install requests
  
This particular version of the code requires the file GoogleNews-vectors-negative300.bin to be present on the user's Desktop. If the file cannot be on the Desktop, Line 44 of Application.py should be changed from reference to '~/Desktop/GoogleNews-vectors-negative300.bin' to the directory in which the Google News vectors file is in.
The Google News file may be found here: 
https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz

# Running the Application
After ensuring all libraries are present and the Google News vectors file in the correct directory (default is desktop), the user should just run Application.py. The program will automatically generate .txt and .csv files, with print statement updates on progress. The program automatically terminates after scores are computed.
