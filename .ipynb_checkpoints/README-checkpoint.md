# LHL-Final-Cat-Personality-Clustering

- Introduction

This is a recommender engine for cat owners that are looking to adopt another cat. The user will rate their cat across 4 trait groups, with the option of seeing cats that are the most similar or least similar in every trait. 

- Dataset

The data is the Domestic Cat Personality Dataset taken from the University of South Australia's domestic cat personality collection. The original dataset consists of 2802 rows and 54 columns. There is one column for Country (New Zeaand or Australia), one column for the cat's sex, and 52 personality trait columns that participants rated from a scale of 1-7. 

- Preprocessing and EDA 

I preprocessed the data by standardizing the column names and removing 38 rows where the `Cat_sex` was either `Null` or `'Unsure'`. I visuallized the distribution of every personality trait to observe for trends. One standout trait was `Eccentric`(image), which had a unique distribution of high values for 1 (the minimum) and 4 (the median), but low values for all the other ratings. It's true that a majority of cats in the dataset could have been not eccentric or average. However, I interpreted this as a lot of users ranking their cat 1 or 4 as a default option because they were unsure of how to answer for this trait, as a cat owner I would do the same thing. Due to this strange distribution I ultimately decided to remove this trait when constructing my recommender. 

I then encoded the `Country` and `Cat_sex` columns and visuallized the pairwise comparisons between all columns. There were no correlations between `Country` and any personality trait, so I also removed that column for my recommender. Even though it also did not correlate with any traits, I chose to keep the `Cat_sex` to give users an option of choosing to see only male/female cats or both. THe personality traits themsevles had correlations as high as r=0.7. The highest correlated traits were. 

Fearful_of_people      Suspicious            0.702191
Suspicious             Trusting             -0.700766
Anxious                Insecure              0.694389
Fearful_of_people      Trusting             -0.664570   

- dimensionality reduction

At this point the data has 51 personality traits. I reduced the data's dimensionality conducting Principle Component Analysis (PCA) and Factor Analysis (FA). I performed PCA first to observe the underlying variance in the data. I created a value `weight` that is the total of all Principle Component loadings squared. I used the `weight` value of each trait to determine the each relevant trait across 5 Principal Components and removed 10 traits that fell under a certrain threshold. 

(image)

I then performed FA to find 



- recommender
- requirements
- 