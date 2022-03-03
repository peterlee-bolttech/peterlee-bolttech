import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import beta
from testResult import testResult
from heatmapResult import heatmapResult
from errorMsg import errorMsg
from pathlib import Path
from PIL import Image

def runVisitorTest():
    test_record = st.file_uploader("Upload Visitor History CSV", type=".csv")
    use_example = st.checkbox(
        "Use example file", False, help="Use in-built example posterior file to demo the app"
    )
    entryGuide = pd.DataFrame(
    {
     'Column Name':['Group', 'Converted'],
     'Column Description':['Test group segmentation', 'Conversion event result of the record'],
        'Exmaple': ['control/test', 'True/False']
    }
)

    st.write("")
    st.write("")
    st.markdown("##### Data Entry Guide - uploaded CSV MUST contain columns as following")
    st.table(entryGuide)

    st.write("")
    st.write("")
    st.markdown("##### Example")
    image = Image.open('./image/visitor_based.png')
    st.image(image)
    # st.image('./image/visitor_based.png')

    st.write("")
    st.markdown("###### *Please tick 'Use example file' to see example format for your reference.")

    if use_example:
        csvLocation = Path(__file__).parents[0] / 'data/visitor_based.csv'
        test_record = csvLocation

    if test_record:
        test_data = pd.read_csv(test_record)

        st.write("")
        st.write("")
        st.markdown("#### Uploaded Data Preview")
        st.dataframe(test_data.head())

        # st.write("")
        # st.write("")
        # st.markdown("#### Select Columns for Analysis")

        # with st.form(key="my_form"):
        #     ab = st.multiselect(
        #         "Select Testing Group Column",
        #         options=test_data.columns,
        #         help="Select which column refers to your control/test testing labels.",
        #         default=ab_default,
        #     )

        #     result = st.multiselect(
        #         "Select Conversion Event Column",
        #         options=test_data.columns,
        #         help="Select which column shows the result of the test.",
        #         default=result_default,
        #     )

        #     st.form_submit_button(label="Submit")

        # if not ab or not result:
        #     st.warning("Please select both an **Testing Group Column** and a **Conversion Event Column**.")
        #     st.stop()

        # name = (
        # "./test_data.csv" if isinstance(test_record, str) else test_record.name
        # )

        try:
            results = test_data.groupby('Group').agg(['count', 'sum'])
            results = results['Converted']
            results.rename({'count': 'sampleSize',
                'sum': 'Converted'}, axis = 1, inplace = True)
            results['conversionRate'] = results['Converted']/results['sampleSize']

            control = beta(1 + results.loc['control', 'Converted'], 1 + results.loc['control', 'sampleSize'] - results.loc['control', 'Converted'])
            test = beta(1 + results.loc['test', 'Converted'], 1 + results.loc['test', 'sampleSize'] - results.loc['test', 'Converted'])

            lower_bound = results['conversionRate'].min() * 0.5
            upper_bound = results['conversionRate'].max() * 1.5

            x = np.linspace(0, 1, 1000)

            testResult(results, x, control, test, lower_bound, upper_bound, 'sampleSize', 'Converted')

            # st.write("")
            # st.write("")
            # st.write("")
            # st.write("")
            # st.write("")
            # st.write("")
            # st.write("")
            # st.write("")
            # heatmapResult(lower_bound, upper_bound, control, test)

        except:
            errorMsg()