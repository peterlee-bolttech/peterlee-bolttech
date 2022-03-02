import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import beta
from testResult import testResult
from heatmapResult import heatmapResult
from errorMsg import errorMsg

def runStoreTest():
    strore_file = st.file_uploader("Upload Sales Record CSV", type=".csv")
    use_store_example_file = st.checkbox(
        "Use example file", False, help="Use in-built example store record file to demo the app"
        )
    entryGuide = pd.DataFrame(
    {
     'Column Name':['Group', 'Phone Sales', 'Device Protection Sales'],
     'Column Description':['Store group segmentation', 'Total number of phone (device) sales during the testing period.', 'Total number of device protection sales during the testing period.'],
        'Exmaple': ['control/test', 'int', 'int']
    }
)

    st.write("")
    st.write("")
    st.markdown("##### Data Entry Guide - uploaded CSV MUST contain columns as following")
    st.table(entryGuide)

    st.write("")
    st.write("")
    st.markdown("##### Example")
    st.image('./store_data.png')

    st.write("")
    st.markdown("###### *Please tick 'Use example file' to see example format for your reference.")

    if use_store_example_file:
        strore_file = "./store_data.csv"

    if strore_file:
        store_data = pd.read_csv(strore_file)

        st.write("")
        st.write("")
        st.markdown("#### Uploaded Data Preview")
        st.dataframe(store_data.head())

        # st.write("")
        # st.write("")
        # st.markdown("#### Select Columns for Analysis")

        # with st.form(key="my_form"):
        #     ab = st.multiselect(
        #         "Select Testing Group Column",
        #         options=store_data.columns,
        #         help="Select which column refers to your control/test labels.",
        #         default=ab_default,
        #     )

        #     result = st.multiselect(
        #         "Select Conversion Event Column",
        #         options=store_data.columns,
        #         help="Select which column shows the result of the test.",
        #         default=result_default,
        #     )

        # st.form_submit_button(label="Submit")

        # if not ab or not result:
        #     st.warning("Please select both an **Testing Group Column** and a **Conversion Event Column**.")
        #     st.stop()

        # name = (
        #     "./store_data.csv" if isinstance(strore_file, str) else strore_file.name
        #     )

        try:
            results = store_data.groupby('Group').agg({'Phone Sales': sum, 'Device Protection Sales': sum})
            results['conversionRate'] = results['Device Protection Sales']/results['Phone Sales']




            control = beta(1 + results.loc['control', 'Device Protection Sales'], 1 + results.loc['control', 'Phone Sales'] - results.loc['control', 'Device Protection Sales'])
            test = beta(1 + results.loc['test', 'Device Protection Sales'], 1 + results.loc['test', 'Phone Sales'] - results.loc['test', 'Device Protection Sales'])

            lower_bound = results['conversionRate'].min() * 0.5
            upper_bound = results['conversionRate'].max() * 1.5

            x = np.linspace(0, 1, 10000)

            testResult(results, x, control, test, lower_bound, upper_bound, 'Phone Sales', 'Device Protection Sales')

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            heatmapResult(lower_bound, upper_bound, control, test)

        except:
            errorMsg()