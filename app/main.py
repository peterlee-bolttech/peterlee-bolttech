from ctypes import alignment
import streamlit as st
from storeApp import runStoreTest
from clickApp import runClickTest

# can only set this once, first thing to set
st.set_page_config(layout="centered") # or 'wide'

# insert bolttech logo with link
st.markdown("[![Foo](https://www.datocms-assets.com/24091/1590561811-bolttech-logo.svg)](http://bolttech.io/)")

with st.container():
    st.header("A/B Testing Tool 📊")
    st.markdown("###### This app helps you analyse A/B testing result by simply plugging in records during test period.")

test_list = (
    'Store-base Attach Rate A/B Test',
    'User-base Click Conversion Rate A/B Test'
)

test_type = st.selectbox("Choose your test type", test_list)

if not test_type:
    st.warning("Please select A/B test kind.")
    st.stop()

if test_type == 'Store-base Attach Rate A/B Test':
    runStoreTest()

elif test_type == 'User-base Click Conversion Rate A/B Test':
    runClickTest()