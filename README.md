# LHL-Final-Cat-Personality-Clustering


This is a recommender engine for cat owners that are looking to adopt another cat. The user will rate their cat across 4 trait groups, with the option of seeing cats that are the most similar or least similar in every trait. 

## Dataset 

The data is the Domestic Cat Personality Dataset taken from the University of South Australia's domestic cat personality collection. The original dataset consists of 2802 rows and 54 columns. There is one column for Country (New Zeaand or Australia), one column for the cat's sex, and 52 personality trait columns that participants rated from a scale of 1-7. 

## Preprocessing and EDA 

I preprocessed the data by standardizing the column names and removing 38 rows where the `Cat_sex` was either `Null` or `'Unsure'`. I visuallized the distribution of every personality trait to observe for trends. One standout trait was `Eccentric`(image), which had a unique distribution of high values for 1 (the minimum) and 4 (the median), but low values for all the other ratings. It's true that a majority of cats in the dataset could have been not eccentric or average. However, I interpreted this as a lot of users ranking their cat 1 or 4 as a default option because they were unsure of how to answer for this trait, as a cat owner I would do the same thing. Due to this strange distribution I ultimately decided to remove this trait when constructing my recommender. 

I then encoded the `Country` and `Cat_sex` columns and visuallized the pairwise comparisons between all columns. There were no correlations between `Country` and any personality trait, so I also removed that column for my recommender. Even though it also did not correlate with any traits, I chose to keep the `Cat_sex` to give users an option of choosing to see only male/female cats or both. THe personality traits themsevles had correlations as high as r=0.7. The highest correlated traits were. 

Fearful_of_people      Suspicious            0.702191
Suspicious             Trusting             -0.700766
Anxious                Insecure              0.694389
Fearful_of_people      Trusting             -0.664570   

## Dimensionality Reduction

At this point the data has 51 personality traits. I reduced the data's dimensionality conducting Principle Component Analysis (PCA) and Factor Analysis (FA). I performed PCA first to observe the underlying variance in the data. I created a value `weight` that is the total of all Principle Component loadings squared. I used the `weight` value of each trait to determine the each relevant trait across 5 Principal Components and removed 10 traits that fell under a certrain threshold. 

(image)

I then performed FA to find reduce the large number of traits into a smaller number of factors based on their underlying patterns. I manually removed some traits that did not positively nor negatively affect any factor, and the final reduced dataset consisted of 4 factors with the following characteristics: 

(image)

1. Anxiety and fearfullness towards humans
- positive: suspicious, insecure, feaful_of_people, anxious, shy
- negative: bold, inquisitive, calm, friendly_to_people, trusting
  
2. Dominance and aggression towards other cats
- positive: defiant, irritable, healous, dominant, reckless, bullying, aggressive_other_cats
- negative: gentle, constrained, friendly_other_cats, submissive

3. Activity level (The values for this trait were originally inverted, I swapped them so higher rating -> higher activity level instead of vice versa)
- positive: vigilant, inquisitive, inventive, smart, curious, playful, decisive, active
- negative: aimless

4. Social Reactivity 

- positive: clumsy, distractable, erratic, impulsive, aimless, excitable
- negative: constrained, smart, deliberate, decisive 

## Recommender Functions 

The `recommender_functions.py` contains the recommender function and some helper functions to help it run successfuly. 

- `input_to_factor`: takes new user ratings from 1-7 and transforms them into the same numeric space as the dataset of cats after dimensionality reduction(determined by each factor's mean and standard deviation)
- `distance`: a custom distance funciton that calculates the distance between two users.  The default is euclidean distance to calculate how similar every factor is between two users, but can be customized so the distances are maximized for factirs that a user wants to see differences in (subtracting the different between two users from the max squared distance for each factor). This function also has a parameter for selecting only specific factors if the user does not want to calculate distances based on all factors.
- `recommend`: The main recommender function. The basic parameters are the rating inputs for the new user and the reduced dataset of cats. The user input is transformed using `input_to_factor`, then `distance` is computed between the new user and every cat in the dataset. The default number of recommendations is 10, and the function outputs the dataset rows along with the computed distance as a match score and a normalized match score to compare between recommendations.
    - advanced parameters can be used to select specific traitsd to compare for similarity or differences. Not all traits need to be used either, and the user can also customize the number of recommendations they wish to see as well as filter for cat_sex in the output. 

- 