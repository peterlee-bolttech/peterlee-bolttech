from ctypes import alignment
import streamlit as st
import warnings
from store_based import runStoreTest
from visitor_based import runVisitorTest

warnings.filterwarnings('ignore')

# can only set this once, first thing to set
st.set_page_config(layout="centered") # or 'wide'

# insert bolttech logo with link
st.markdown("[![Foo](https://www.datocms-assets.com/24091/1590561811-bolttech-logo.svg)](http://bolttech.io/)")

with st.container():
    st.header("A/B Testing Tool 📊")
    st.markdown("###### This app helps you analyse A/B testing result by simply plugging in records during test period.")

test_list = (
    'Store-based Attach Rate A/B Test',
    'Visitor-based Conversion Rate A/B Test'
)

test_type = st.selectbox("Choose your test type", test_list)

if not test_type:
    st.warning("Please select A/B test kind.")
    st.stop()

if test_type == 'Store-based Attach Rate A/B Test':
    runStoreTest()

elif test_type == 'Visitor-based Conversion Rate A/B Test':
    runVisitorTest()