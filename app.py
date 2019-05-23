#!/usr/bin/env python3

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd
import numpy as np
import csv

### CONFIG
# wz: given 7 hours a day for work, friday for learning, targets are
# 7 for learning a week
# 7 * 4 days for work
# 1 for jogging
# 1 hr a night for finance * 4
qnArr = [
    {'cat': 'work', 'qn': 'How much time did you spend at work today?', 'targetPerWeek': 28},
    {'cat': 'learn',
     'qn': 'How much time did you spend learning today?', 'targetPerWeek': 7},
    {'cat': 'finance', 'qn': 'How much time did you spend on finance research today?',
     'targetPerWeek': 4},
    {'cat': 'health', 'qn': 'How much time did you spend jogging today?',
     'targetPerWeek': 1}
]

### WRITING CSV AND TXT
print('Hello wz')
print('Today is ' + str(datetime.now()))
print('Hope you had a productive day!')

file = open("workJnl.txt", "a+")
file.write(str(datetime.now()) + '\r')
for each in qnArr:
    ans = input(each['qn'])
    file.write(each['cat'] + ': ' + ans + '\r')

    with open('workJnlCSV.csv', mode='a+') as workJnlCSV:
      writer = csv.writer(
        workJnlCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      writer.writerow([datetime.now().date(), each['cat'], ans])
comments = input('Any notes for today?')
file.write(comments + '\r')
file.close()

### PLOTTING
df = pd.read_csv('./workJnlCSV.csv', header=None, index_col=0, parse_dates=True)
df.columns = ['cat', 'hourPerDay']
df.index.name = 'date'

# # filter for right dates (7 days) NOT NEEDED
# weeklyDf = df[(df['date'] <= str(datetime.today())) & (df['date'] > str(datetime.today() - timedelta(days=7)))]
# print("weekly")
# print(weeklyDf)

# pivot to sum all hours for the week
pivotTable = pd.pivot_table(df, values='hourPerDay', index='date', columns='cat', aggfunc=np.sum)
print("pivot table")
print(pivotTable)

# resampled to weekly
weeklyDf = pivotTable.resample('W').sum()
print("resampled into weekly")
print(weeklyDf)

# trigger print pie graph function by week
labels = weeklyDf.tail(1).columns.values
sizes = weeklyDf.tail(1).values[0]
print(labels, sizes)

# Plot pie
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'] # assumes only 4 categories
explode = (0, 0, 0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show()

# Plot bar chart with 'target'
n_groups = labels.size
actual = (sizes)
qnArrSorted = sorted(qnArr, key=lambda x: x['cat'], reverse=False)
targetPerCat = []
for each in qnArrSorted:
  targetPerCat.append(each['targetPerWeek'])

target = (targetPerCat)
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
# error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, actual, bar_width,alpha=opacity, color='b', label='Actual')
rects2 = ax.bar(index + bar_width, target, bar_width, alpha=opacity, color='r', label='Target')

ax.set_xlabel('Category')
ax.set_ylabel('Hours')
ax.set_title('Hours by category per week')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels((labels))
ax.legend()

fig.tight_layout()
plt.show()


# TODO: 
# what to do with other things i like...
# open source contribution, writing medium article, training hackerrank
