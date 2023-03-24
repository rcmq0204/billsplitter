#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 21:21:41 2023

@author: rcmq0204
"""

import streamlit as st

st.title('Bill Splitting App')
st.markdown('This app helps to calculate the amount each person has to pay in the bill :)')
st.write('Click the following checkboxes if there is GST and/or SVC:')
if st.checkbox('GST'):
    GST=st.number_input('Enter the GST in %% here (if GST is 8%, type 8)')
    st.write('The GST is ',GST,'%')
else:
    GST=0
    st.write('The GST is ',GST,'%')

if st.checkbox('SVC'):
    SVC=st.number_input('Enter the SVC in %% here (if SVC is 10%, type 10)')
    st.write('The SVC is ',SVC,'%')
else:
    SVC=0
    st.write('The SVC is ',SVC,'%')














    


        


