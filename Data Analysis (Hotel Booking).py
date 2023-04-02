#!/usr/bin/env python
# coding: utf-8

# # Business Problem
# 
# In recent years, City Hotel and Resort Hotel have seen high cancellation rates. Each
# 
# hotel is now dealing with a number of issues as a result, including fewer revenues and
# less than ideal hotel room use. Consequently, lowering cancellation rates is both hotels'
# primary goal in order to increase their efficiency in generating revenue, and for us to
# offer thorough business advice to address this problem.
# The analysis of hotel booking cancellations as well as other factors that have no bearing
# on their business and yearly revenue generation are the main topics of this report.

# # Import Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the dataset
# 

# In[6]:


df = pd.read_csv("hotel_bookings 2.csv")


# # Exploratory Data Analysis and Data Cleaning

# In[9]:


df.head()


# In[12]:


df.tail(6)


# In[13]:


df.shape


# In[17]:


df.columns


# In[18]:


df.info()


# In[19]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[20]:


df.info()


# In[21]:


df.describe(include='object')


# In[26]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print("--"*30)


# In[27]:


df.isnull().sum()


# In[28]:


df.drop(['company','agent'],axis =1,inplace=True)
df.dropna(inplace=True)


# In[29]:


df.isnull().sum()


# In[33]:


df.describe()


# In[32]:


df = df[df['adr']<5000]


# # Data Analysis and Visualizations
# 

# The accompanying bar graph shows the percentage of reservations that are canceled
# and those that are not. It is obvious that there are still a significant number of
# reservations that have not been canceled. There are still 37% of clients who canceled
# their reservation, which has a significant impact on the hotels' earnings.

# In[38]:


cancelled_perc = df['is_canceled'].value_counts(normalize=True)
print(cancelled_perc)

plt.figure(figsize= (6,5))
plt.title("Reservation Status Count")
plt.bar(['Not canceled','Canceled'],df['is_canceled'].value_counts(),edgecolor = 'k',width=0.7)
plt.show()


# In comparison to resort hotels, city hotels have more bookings. It's possible that resort
# hotels are more expensive than those in cities.

# In[102]:


plt.figure(figsize=(6,5))

ax1 = sns.countplot(x='hotel',hue='is_canceled',data=df,palette="Blues")

legend_labels = ax1.get_legend_handles_labels()
ax1.legend(['not canceled','canceled'])
plt.title("Reservation sates in different hotels", size= 20)
plt.xlabel("Hotel")
plt.ylabel("Number of reservations")
plt.show()


# In[65]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize =True)


# In[74]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize =True)


# In[79]:


resort_hotel=resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[58]:


df.columns


# The line graph above shows that, on certain days, the average daily rate for a city hotel
# is less than that of a resort hotel, and on other days, it is even less. It goes without
# saying that weekends and holidays may see a rise in resort hotel rates.

# In[88]:


plt.figure(figsize=(20,9))
plt.title("Average Daily Rate in City and Resort Hote",size=25)

plt.plot(resort_hotel.index,resort_hotel['adr'],label ='Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'],label ='City Hotel')
plt.legend(fontsize=20)
plt.show()


# We have developed the grouped bar graph to analyze the months with the highest and
# lowest reservation levels according to reservation status. As can be seen, both the
# number of confirmed reservations and the number of canceled reservations are largest
# in the month of August. whereas January is the month with the most canceled
# reservations.

# In[105]:


# df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize=(20,9))
ax1 = sns.countplot(x=df['month'],hue='is_canceled',data=df)
ax1.legend(['not canceled','canceled'],fontsize=20)
plt.show()


# This bar graph demonstrates that cancellations are most common when prices are
# greatest and are least common when they are lowest. Therefore, the cost of the
# accommodation is solely responsible for the cancellation.

# In[123]:


plt.figure(figsize=(15,8))
plt.title('ADR per month',size=30)
a = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index()

sns.barplot(x='month',y='adr',data=a)


# Now, let's see which country has the highest reservation canceled. The top country is
# Portugal with the highest number of cancellations.

# In[138]:


canceled_Data  = df[df['is_canceled']==1]
top_10_country = canceled_Data['country'].value_counts()[:10]

plt.figure(figsize =(8,8))
plt.title("Top 10 countries with reservation canceled")
plt.pie(top_10_country,autopct= ' %.2f',labels=top_10_country.index)
plt.show()
                                                        


# In[140]:


df['market_segment'].value_counts()


# In[141]:


df['market_segment'].value_counts(normalize=True)


# In[145]:


canceled_Data['market_segment'].value_counts(normalize = True)


# In[160]:


cancelled_df_Adr =  canceled_Data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_Adr.reset_index(inplace=True)
cancelled_df_Adr.sort_values("reservation_status_date",inplace=True)

not_canceled_data  = df[df['is_canceled']==0]
not_canceled_df_adr = not_canceled_data.groupby('reservation_status_date')[['adr']].mean()
not_canceled_df_adr.reset_index(inplace=True)
not_canceled_df_adr.sort_values('reservation_status_date',inplace =True)

plt.figure(figsize=(20,6))
plt.title("Average Daily Rate",size=25)
plt.plot(not_canceled_df_adr['reservation_status_date'],not_canceled_df_adr['adr'],label ='not canceled')
plt.plot(cancelled_df_Adr['reservation_status_date'],cancelled_df_Adr['adr'],label ='canceled')
plt.legend(fontsize=20)
plt.show()


# In[155]:


cancelled_df_adr = cancelled_df_Adr[(cancelled_df_Adr['reservation_status_date']>'2016')&(cancelled_df_Adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_canceled_df_adr[(not_canceled_df_adr['reservation_status_date']>'2016')&(not_canceled_df_adr['reservation_status_date']<'2017-09')]


# As seen in the graph, reservations are canceled when the average daily rate is higher
# than when it is not canceled. It clearly proves all the above analysis, that the higher
# price leads to higher cancellation.

# In[161]:


plt.figure(figsize=(20,6))
plt.title("Average Daily Rate",size=25)
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label ='not canceled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label ='canceled')
plt.legend(fontsize=20)
plt.show()


# # Suggestions
# 
# Suggestions
# 
# 1. Cancellation rates rise as the price does. In order to prevent cancellations of
# reservations, hotels could work on their pricing strategies and try to lower the
# rates for specific hotels based on locations. They can also provide some
# discounts to the consumers.
# 2. As the ratio of the cancellation and not cancellation of the resort hotel is higher in
# the resort hotel than the city hotels. So the hotels should provide a reasonable
# discount on the room prices on weekends or on holidays.
# 3. In the month of January, hotels can start campaigns or marketing with a
# reasonable amount to increase their revenue as the cancellation is the highest in
# this month.
# 4. They can also increase the quality of their hotels and their services mainly in
# Portugal to reduce the cancellation rate.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




