import streamlit as st
import pandas as pd
import numpy as np
import decimal
from scipy.stats import beta
from posterior import posterior_plot
from heatmap import heatmap_plot

def runStoreTest():

    strore_file = st.file_uploader("Upload Sales Record CSV", type=".csv")
    use_store_example_file = st.checkbox(
        "Use example file", False, help="Use in-built example store record file to demo the app"
        )

    if use_store_example_file:
        strore_file = "./store_data.csv"
        ab_default = ['Group']
        result_default = ['Device Protection Sales']

    if strore_file:
        store_data = pd.read_csv(strore_file)
        ab_default = None
        result_default = None

        st.write("")
        st.write("")
        st.markdown("#### Uploaded Data Preview")
        st.dataframe(store_data.head())

        st.write("")
        st.write("")
        st.markdown("#### Select Columns for Analysis")

        with st.form(key="my_form"):
            ab = st.multiselect(
                "Select Testing Group Column",
                options=store_data.columns,
                help="Select which column refers to your control/test labels.",
                default=ab_default,
            )
            if ab:
                control = store_data[ab[0]].unique()[0]
                test = store_data[ab[0]].unique()[1]

                visitors_a = store_data[ab[0]].value_counts()[control]
                visitors_b = store_data[ab[0]].value_counts()[test]

            result = st.multiselect(
                "Select Conversion Event Column",
                options=store_data.columns,
                help="Select which column shows the result of the test.",
                default=result_default,
            )

            if result:
                conversions_a = (
                    store_data[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][control]
                )
                conversions_b = (
                    store_data[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][test]
                )

            submit_button = st.form_submit_button(label="Submit")

        if not ab or not result:
            st.warning("Please select both an **Testing Group Column** and a **Conversion Event Column**.")
            st.stop()


        name = (
            "./store_data.csv" if isinstance(strore_file, str) else strore_file.name
            )

        results = store_data.groupby('Group').agg({'Phone Sales': sum, 'Device Protection Sales': sum})
        results['conversionRate'] = results['Device Protection Sales']/results['Phone Sales']

        # bayes-laplace
        prior_alpha = 1
        prior_beta = 1

        control = beta(prior_alpha + results.loc['control', 'Device Protection Sales'], prior_beta + results.loc['control', 'Phone Sales'] - results.loc['control', 'Device Protection Sales'])
        test = beta(prior_alpha + results.loc['test', 'Device Protection Sales'], prior_beta + results.loc['test', 'Phone Sales'] - results.loc['test', 'Device Protection Sales'])


        lower_bound = results['conversionRate'].min() * 0.5
        upper_bound = results['conversionRate'].max() * 1.5

        x = np.linspace(0, 1, 1000)

        st.write("")
        st.write("")
        st.markdown("#### Test Result Summary")
        st.dataframe(results)
        with st.container():
            plot = posterior_plot(x, control.pdf(x), test.pdf(x), lower_bound, upper_bound)
            st.plotly_chart(plot)

        decimal.getcontext().prec = 4
        control_simulation = np.random.beta(prior_alpha + results.loc['control', 'Device Protection Sales'], prior_beta + results.loc['control', 'Phone Sales'] - results.loc['control', 'Device Protection Sales'], size=10000)
        test_simulation = np.random.beta(prior_alpha + results.loc['test', 'Device Protection Sales'], prior_beta + results.loc['test', 'Phone Sales'] - results.loc['test', 'Device Protection Sales'], size=10000)
        test_won = [i <= j for i,j in zip(control_simulation, test_simulation)]
        chance_of_beating_control = np.mean(test_won)

        st.write("")
        st.write("")
        st.markdown(f'### Chance of test beating control is {decimal.getcontext().create_decimal(chance_of_beating_control) * 100} %')

        joint_dist_for_plot = []
        for i in np.linspace(lower_bound,upper_bound,100):
            for j in np.linspace(lower_bound, upper_bound, 100):
                joint_dist_for_plot.append([i, j, control.pdf(i)*test.pdf(j)])
        joint_dist_for_plot = pd.DataFrame(joint_dist_for_plot)
        joint_dist_for_plot.rename({0: 'control_cr', 1: 'test_cr', 2: 'joint_density'}, axis=1, inplace=True)
        tick_locations = range(0, 160, 10)
        tick_labels = [round(0.26 + i*0.01, 2) for i in range(16)]
        heatmap_df = pd.pivot_table(joint_dist_for_plot, values='joint_density', index='test_cr', columns='control_cr')

        st.write("")
        st.write("")
        st.markdown("#### Joint Distribution")
        with st.container():
            plot = heatmap_plot(heatmap_df)
            st.plotly_chart(plot)