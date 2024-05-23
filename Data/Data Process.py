import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Read Facebook data file
with open('facebook_data.json', 'r', encoding='utf-8') as f:
    facebook_data = json.load(f)

# Read Twitter data file
with open('twitter_data.json', 'r', encoding='utf-8') as f:
    twitter_data = json.load(f)

# Convert Facebook data to DataFrame
facebook_df = pd.json_normalize(facebook_data)

# Process Facebook data
facebook_df['post_datetime'] = pd.to_datetime(facebook_df['post_datetime'])
facebook_df['post_file.image'] = facebook_df['post_file.image'].apply(lambda x: x[0]['link'] if len(x) > 0 else 'no_image')

# Extract text information from Facebook data
facebook_texts = facebook_df['caption'].tolist()

# Convert Twitter data to DataFrame
twitter_df = pd.json_normalize(twitter_data['results'])

# Process Twitter data
twitter_df['media_url'] = twitter_df['media_url'].fillna('no_media')
twitter_df['creation_date'] = pd.to_datetime(twitter_df['creation_date'])

# Extract text information from Twitter data
twitter_texts = twitter_df['text'].tolist()

# Combine all text data
all_texts = facebook_texts + twitter_texts

# Create Bag-of-Words model
vectorizer_bow = CountVectorizer()
X_bow = vectorizer_bow.fit_transform(all_texts)

# Create TF-IDF model
vectorizer_tfidf = TfidfVectorizer()
X_tfidf = vectorizer_tfidf.fit_transform(all_texts)

# Convert Bag-of-Words feature matrix to DataFrame
df_bow = pd.DataFrame(X_bow.toarray(), columns=vectorizer_bow.get_feature_names_out())

# Convert TF-IDF feature matrix to DataFrame
df_tfidf = pd.DataFrame(X_tfidf.toarray(), columns=vectorizer_tfidf.get_feature_names_out())

# Save Bag-of-Words features to CSV file
df_bow.to_csv('bow_features.csv', index=False)

# Save TF-IDF features to CSV file
df_tfidf.to_csv('tfidf_features.csv', index=False)

print("Bag-of-Words features saved to bow_features.csv")
print("TF-IDF features saved to tfidf_features.csv")
