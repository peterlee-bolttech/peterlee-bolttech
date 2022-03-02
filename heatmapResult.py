import streamlit as st
import numpy as np
import pandas as pd
from heatmap import heatmap_plot

def heatmapResult(lower_bound, upper_bound, control, test):
    joint_dist_for_plot = []
    for i in np.linspace(lower_bound,upper_bound,100):
        for j in np.linspace(lower_bound,upper_bound,100):
            joint_dist_for_plot.append([i, j, control.pdf(i)*test.pdf(j)])
    joint_dist_for_plot = pd.DataFrame(joint_dist_for_plot)
    joint_dist_for_plot.rename({0: 'control_cr', 1: 'test_cr', 2: 'joint_density'}, axis=1, inplace=True)


    heatmap_df = pd.pivot_table(joint_dist_for_plot, values='joint_density', index='test_cr', columns='control_cr')
    st.write("")
    st.write("")
    st.markdown("#### Joint Distribution")
    with st.container():
        plot = heatmap_plot(heatmap_df)
        st.plotly_chart(plot)