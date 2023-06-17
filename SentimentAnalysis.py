import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from Scraper import Reviews

plt.style.use('ggplot')

vest = Reviews('https://www.amazon.ca/Floating-OMOUBOI-Swimming-Snorkeling-Inflatable/dp/B08K32JFR7/ref=cm_cr_arp_d_product_top?ie=UTF8')
vest.get_all_reviews()


df = pd.DataFrame.from_dict(vest.reviews)

low_rating = df[(df['rating'] >= 0) & (df['rating'] <= 2)]

print(low_rating)
