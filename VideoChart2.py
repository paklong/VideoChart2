import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('fivethirtyeight')

pd.options.display.max_rows = None

data = pd.read_csv('master.csv')
dataProcessed = data.groupby(['year', 'country']).agg({'suicides_no':'sum'}).reset_index()

r = lambda: random.randint(0,255)
color = [('#%02X%02X%02X' % (r(),r(),r())) for i in range(101)]
country = dataProcessed.country.unique()

colors = pd.DataFrame(list(zip(country, color)), columns =['country', 'color']) 
dataProcessed = dataProcessed.merge(colors, on = 'country')
dataProcessed[dataProcessed.year == 1985].sort_values(by = 'suicides_no', ascending = False)

def draw(year):
    ax.clear()
    _year = dataProcessed[dataProcessed.year == year].sort_values(by = 'suicides_no', ascending = False)
    _year = _year.head(10).sort_values(by = 'suicides_no', ascending = True)
    ax.barh(_year['country'], _year['suicides_no'], color=_year['color'])
    
    for i, (value, country) in enumerate(zip(_year['suicides_no'], _year['country'])):
        ax.text(value, i, " "+str(value), va='center', fontsize=20)

    ax.text(1, 0.1, year, transform=ax.transAxes, color='#a9a9a9', size=46, ha='right', weight=800)
    ax.set_title('Suicide Rates Overview 1985 to 2016', fontsize=40, weight='bold')
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=20)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(20)
        tick.label1.set_fontweight('bold')
    ax.yaxis.grid(False) # horizontal lines
    ax.xaxis.grid(True) # vertical lines    
    plt.tight_layout()
    plt.show()


fig, ax = plt.subplots(figsize=(16,9))
animator = animation.FuncAnimation(fig, draw, frames=range(1985, 2015), interval=500)
animator.save('animator.mp4', bitrate=20000)
