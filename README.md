# Fake Review Detection

# Business Problem

How many times have you read reviews while searching for places to eat and not thinking twice about whether or not the review was left by a real person? I would think that answer is very often. Most of the time, we make snap decisions on a few of the reviews. Fake reviews can falsely hurt or boost a restaurants reputation on a review website, and deter customers from visiting restaurants. An extra star on somewhere like Yelp can increase revenue by 5-9 percent. This is false advertising. The intergity of the site is important, and people need to be able to trust the reviews they read. There are places you can go to purchase reviews for a business. https://www.youtube.com/watch?v=KdG81QKdga0 is a video showing how reviews can be bought or sold. There needs to be a barrier in place in order to detect this fraudulent behavior.
 
A model using NLP(Natural Language Processing) can be used to flag reviews as they are posted to be peer reviewed by a person. Since this is designed to flag a review to be peer reviewed, it will be better for the model to predict more false positives (or reviews that the model thinks is fake but is not). False negatives are something to avoid. This type of scoring will want to maximize recall. This model can help protect any review website wanting to improve review integrity.

# Data

Over 110k rows of data obtained from a data set located on kaggle. This data is labelled as real reviews and fake reviews. Current data was also scraped from Yelp.

![image](https://user-images.githubusercontent.com/82483702/138175801-4a677897-5510-4cf0-be47-11e4a4b5443c.png)

This is the distribution of the data in the dataset from Yelp.


# EDA

In a quick overview, the reviews labelled  fake are usually shorter than the reviews labelled as real. Perhaps this could be because the star rating is more important than the actual review itself. This would make sense if a review were bought just for a boosted star. The reviewer would put less effort into writing the review because they know it does not really matter, plus they have to make up experiences which take more effort than is worth. People with real reviews will have no problem describing their experience because the experience actually happened.

![image](https://user-images.githubusercontent.com/82483702/138177886-4ba1867f-1702-4d06-b982-37c68d94f587.png)

![image](https://user-images.githubusercontent.com/82483702/138177906-ab9f8c4e-ae06-4f5c-8b03-87201e388c91.png)

Better images will be added and go into more detail about the words used in real vs fake reviews.

# Model

A TFIDF Vectorizer with the minority class over sampled utilizing an XGBoost model has given the best results so far. Recall score of 56.4

![image](https://user-images.githubusercontent.com/82483702/138178082-5b953050-c042-41c0-9bb2-d45118a6df9d.png)

# Conlcusion

With the help of machine learning and natural language processing, the problem of fake reviews can be minimized. With access to more data such as user activity and the location of the user are things that could further help the model catch fake reviews. 




