import streamlit as st
import decimal
import numpy as np
from posterior import posterior_plot
from barplot import barplot

def testResult(results, x, control, test, lower_bound, upper_bound, sampleSize, converted):
    st.write("")
    st.write("")
    st.markdown("#### Test Result Summary📈")
    st.dataframe(results)

    with st.container():
        plot = barplot(results, sampleSize, converted)
        st.plotly_chart(plot)

    with st.container():
        plot = posterior_plot(x, control.pdf(x), test.pdf(x), lower_bound, upper_bound)
        st.plotly_chart(plot)

    decimal.getcontext().prec = 4
    num_simulation = 50000
    control_simulation = np.random.beta(1 + results.loc['control', converted], 1 + results.loc['control', sampleSize] - results.loc['control', converted], size=num_simulation)
    test_simulation = np.random.beta(1 + results.loc['test', converted], 1 + results.loc['test', sampleSize] - results.loc['test', converted], size=num_simulation)
    test_won = [i <= j for i,j in zip(control_simulation, test_simulation)]
    chance_of_beating_control = np.mean(test_won)

    st.write("")
    st.write("")
    st.markdown(f'## Test Result💻')
    st.markdown(f'### After *{num_simulation}* times of simulations, chance of test beating control is *{decimal.getcontext().create_decimal(chance_of_beating_control) * 100}* %')