import pandas as pd
import matplotlib.pyplot as plt

# Data Prep
csv_file = 'high_chart_raw_data.csv'
raw_data = pd.read_csv(csv_file)
raw_data['month'] += 1
monthly_metrics = raw_data.sort_values(['year', 'month']).reset_index(drop=True)

# 1_purchases bar chart by month
monthly_purchases = monthly_metrics[['year', 'month', 'n_members', 'n_occasional']]
monthly_purchases = monthly_purchases.set_index(['year', 'month'])
monthly_purchases.columns = ['Members', 'Occasionals']
monthly_purchases.plot.barh(stacked=True, color=['#eb483c', '#2c313e'])
plt.gca().invert_yaxis()
plt.grid(axis='x', color='#D8D8D8', linestyle='-', linewidth=0.5)
plt.title('# Purchases of Memberships and Short-term Access')
plt.xlabel('Number of users')
plt.savefig('1_purchases bar chart by month.png')
plt.close()

# 2_trips bar chart by month
monthly_trips = monthly_metrics[['year', 'month', 'n_rides_members', 'n_rides_occasional']]
monthly_trips = monthly_trips.set_index(['year', 'month'])
monthly_trips.columns = ['# Trips by members', '# Trips by occasionals']
monthly_trips.plot.barh(stacked=True, color=['#eb483c', '#2c313e'])
plt.gca().invert_yaxis()
plt.grid(axis='x', color='#D8D8D8', linestyle='-', linewidth=0.5)
plt.title('# Trips of Members and Occasionals')
plt.xlabel('Number of trips')
plt.savefig('2_trips bar chart by month.png')
plt.close()

# 3_Block view per year
year_metrics = monthly_metrics.groupby('year').sum()
year_metrics['n_purchases'] = year_metrics['n_members'] + year_metrics['n_occasional']
year_metrics['n_trips'] = year_metrics['n_rides_members'] + year_metrics['n_rides_occasional']
year_metrics['pct_members'] = year_metrics['n_members'] / year_metrics['n_purchases']
year_metrics['pct_occasional'] = year_metrics['n_occasional'] / year_metrics['n_purchases']
year_metrics['pct_trips_members'] = year_metrics['n_rides_members'] / year_metrics['n_trips']
year_metrics['pct_trips_occasional'] = year_metrics['n_rides_occasional'] / year_metrics['n_trips']
print(year_metrics)

year_list = year_metrics.index
ax_list = ['ax1', 'ax2', 'ax3', 'ax4']
fig, (ax_list) = plt.subplots(1, 4, figsize=(18, 4))
for i in range(len(year_list)):
    yr = year_list[i]
    ax_list[i].set(title=year_list[i])
    ax_list[i].stackplot([0, 1], [1, 1], color=['#2c313e'])
    if i == len(year_list) - 1:
        ax_list[i].text(0.03, 0.85, 'Occasionals', color='w')
        ax_list[i].text(0.03, 0.1, 'Members', color='w')
    ax_list[i].text(0.03, 0.9, "{0:.0f}%".format(year_metrics.at[yr, 'pct_occasional'] * 100), color='w')
    ax_list[i].text(0.03, 0.05, "{0:.0f}%".format(year_metrics.at[yr, 'pct_members'] * 100), color='w')
    ax_list[i].stackplot([0, 1], [year_metrics.at[yr, 'pct_members'],
                                  year_metrics.at[yr, 'pct_trips_members']], color=['#eb483c'])
    ax_list[i].text(0.85, 0.9, "{0:.0f}%".format(year_metrics.at[yr, 'pct_trips_occasional'] * 100), color='w')
    ax_list[i].text(0.85, 0.05, "{0:.0f}%".format(year_metrics.at[yr, 'pct_trips_members'] * 100), color='w')
    ax_list[i].axes.get_xaxis().set_visible(False)
    ax_list[i].grid(color='w', linestyle='-', linewidth=0.3)

plt.title('% Purchases', loc='left')
plt.title('% Trips', loc='right')
plt.savefig('3_yearly block.png')
plt.close()

# 4_Line view in one chart
fig, ax = plt.subplots()
x = [0, 1]
y = [None] * 4
alpha_list = [0.1, 0.35, 0.65, 1]
for i in range(len(year_list)):
    y[i] = [year_metrics.at[year_list[i], 'pct_members'], year_metrics.at[year_list[i], 'pct_trips_members']]
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.set_xlim([0, 1])
    ax.axes.set_ylim([0, 1])
    plt.plot(x, y[i], color='r', alpha=alpha_list[i], marker='o', label=year_list[i])
plt.legend()
plt.title('% Purchases of Members', loc='left')
plt.title('% Trips of Members', loc='right')
plt.savefig('4_line chart in one.png')
plt.close()
