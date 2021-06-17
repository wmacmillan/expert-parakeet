#!/usr/bin/env python
# coding: utf-8
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)


# In[6]:


import pandas as pd
import datetime
from finquant.portfolio import build_portfolio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from finquant.efficient_frontier import EfficientFrontier
# plotting style:
plt.style.use("seaborn-darkgrid")
# set line width
plt.rcParams["lines.linewidth"] = 2
# set font size for titles
plt.rcParams["axes.titlesize"] = 14
# set font size for labels on axes
plt.rcParams["axes.labelsize"] = 12
# set size of numbers on x-axis
plt.rcParams["xtick.labelsize"] = 10
# set size of numbers on y-axis
plt.rcParams["ytick.labelsize"] = 10
# set figure size
plt.rcParams["figure.figsize"] = (10, 6)


# ## Throw on some stocks

# In[7]:



d = {
    0: {"Name": "WIKI/GOOG", "Allocation": 20},
    1: {"Name": "WIKI/AMZN", "Allocation": 10},
    2: {"Name": "WIKI/MCD", "Allocation": 15},
    3: {"Name": "WIKI/DIS", "Allocation": 18},
}


# ### Run everything.

# In[8]:

pf_allocation = pd.DataFrame.from_dict(d, orient="index")
names = pf_allocation["Name"].values.tolist()

# dates can be set as datetime or string, as shown below:
start_date = datetime.datetime(2015, 1, 1)
end_date = "2017-12-31"
pf = build_portfolio(
    names=names, pf_allocation=pf_allocation, start_date=start_date, end_date=end_date
)


# ### Show the tear sheet.

# In[10]:


st.write(pf.properties())


# ### Optimize the thing.

# In[11]:


# creating an instance of EfficientFrontier
ef = EfficientFrontier(pf.comp_mean_returns(freq=1), pf.comp_cov())
# optimisation for minimum volatility
st.write(ef.minimum_volatility())

# printing out relevant quantities of the optimised portfolio
(expected_return, volatility, sharpe) = ef.properties(verbose=True)

# #### Efficient Frontier of `pf`

# computing and plotting efficient frontier of pf
pf.ef_plot_efrontier()
# adding markers to optimal solutions
pf.ef_plot_optimal_portfolios()
# and adding the individual stocks to the plot
fig = pf.plot_stocks()
# plt.show()
st.pyplot(fig)

