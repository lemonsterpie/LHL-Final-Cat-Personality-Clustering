from sklearn.metrics import pairwise_distances
import pandas as pd 
import numpy as np
import os 


DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'data_reduced.csv')
data = pd.read_csv(DATA_PATH)

factors = ['Factor1', 'Factor2', 'Factor3', 'Factor4']
traits = data[factors]

means = np.array(traits.mean())
stds = np.array(traits.std())
max_dists_sq = (traits.max() - traits.min()) ** 2


def input_to_factor(user_input):
    """
    Transforms a new user's 1–7 input into the same scale as factor scores.
    """
    # Convert 1–7 scale to z-score-like values in range [-3, 3]
    user_input = np.array(user_input)
    z_approx = (user_input - 4) * (6 / 6)  # i.e., 1 -> -3, 4 -> 0, 7 -> +3

    # Map z_approx into the actual distribution of factor scores
    transformed = z_approx * stds + means
    return transformed


def distance(user1, user2, same_traits=None, different_traits=None, factors=None):

    if factors is not None:
        user1 = pd.Series(user1, index=factors)
        user2 = pd.Series(user2, index=factors)
    else:
        user1 = pd.Series(user1)
        user2 = pd.Series(user2)
        
    diff = user1 - user2 
    dist = 0.0
    n = len(user1)

    # if no traits are specified to be similar or different, the default is to recommend based on similarities in all traits 

    if same_traits is None and different_traits is None:
        same_traits = user1.index
        different_traits = []
        
    elif same_traits is None:
        same_traits = [i for i in user1.index if i not in different_traits]
        
    elif different_traits is None:
        different_traits = [i for i in user1.index if i not in same_traits]

    elif same_traits is not None:
        same_traits = [t for t in same_traits if t in factors]
    
    elif different_traits is not None:
        different_traits = [t for t in different_traits if t in factors]
        
    for i in same_traits:
        dist += diff.loc[i] ** 2

    for i in different_traits:
        max_val = max_dists_sq.loc[i]
        dist += (max_val - diff.loc[i] ** 2)

    return dist

def recommend(new_user, data, same_traits=None, different_traits=None, n_recs=10, factors=None, sex='all'):
    
    distances = []

    # Factor names must match data columns
    all_factors = ['Factor1', 'Factor2', 'Factor3', 'Factor4']

    if factors is None:
        factors = all_factors

    # Convert user input to Series with labels matching data
    new_user = pd.Series(input_to_factor(new_user), index=all_factors)

    # Filter both user and dataset to selected factors
    new_user = new_user[factors] 
    data_filtered = data[factors + ['Cat_sex']]

    for i, row in data_filtered.iterrows(): 
        user2 = np.array(row[factors], dtype=float)
        d = distance(new_user, user2, same_traits, different_traits, factors)
        distances.append((i, d))
    
    all_scores = [dist for _, dist in distances]  # all distances computed
    global_min = min(all_scores)
    global_max = max(all_scores)
    score_range = global_max - global_min if global_max != global_min else 1
    
    if sex != 'all':
        valid_indices = data[data['Cat_sex'] == sex].index
        distances = [(i, d) for i, d in distances if i in valid_indices]
    
    distances.sort(key=lambda x: x[1])
    top_indices = [idx for idx, _ in distances[:n_recs]]
    top_distances = [dist for _, dist in distances[:n_recs]]

    top_rows = data_filtered.loc[top_indices].copy()
    top_rows['match_score'] = top_distances
    top_rows['match_score_normalized'] = [
    (score - global_min) / score_range for score in top_distances
]
    return top_rows