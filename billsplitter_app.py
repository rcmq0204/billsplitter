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

def name_adder(name:str):
    if name not in st.session_state.names:
        st.session_state.names.append(name)
    else:
        st.warning(f'This name has already been addded')
    if name not in st.session_state.people_price:
        st.session_state.people_price[name]=0

def name_deleter(name:str):
    st.session_state.names.remove(name)

def price_adder(price:float):
    if price<0:
        st.warning(f'Please enter a proper price')
    else:
        st.session_state.prices.append(price)

def people_price_adder(people:list,price:float):
    ppp=price/len(people) #ppp=price per person
    for i in people:
        st.session_state.people_price[i]+=ppp
        
def gst_svc_adder(GST:float,SVC:float):
    for key in st.session_state.people_price:
        st.session_state.people_price[key]=round(st.session_state.people_price[key]*(1+GST/100)*(1+SVC/100),2)

if 'names' not in st.session_state:
    st.session_state.names=[] #list of names

if 'prices' not in st.session_state:
    st.session_state.prices=[] #list of prices

if 'people_price' not in st.session_state:
    st.session_state.people_price={}

name=st.text_input('Enter name here (one at a time)',key='new_name')
st.button('Add name',key='button_add_name',on_click=name_adder,args=(name,))

name_del=st.selectbox('Select name you wish to delete',st.session_state.names)
st.write('Check and confirm then click the delete button')
st.button('Delete',key='name_del',on_click=name_deleter,args=(name_del,))
    
st.write(st.session_state.names)
st.write('Ensure that all names are added above')

price=st.number_input('Enter price of food',format='%.2f')
st.button('Enter Price',key='price_add',on_click=price_adder,args=(price,))
people=st.multiselect('Select who will split this price',options=st.session_state.names,default=st.session_state.names)
st.button('Split among these people^',key='button_splitter',on_click=people_price_adder,args=(people,price))

#once all the prices have been split, need to add gst and svc
st.button('Compute amounts with GST and SVC',key='gst_svc_adder',on_click=gst_svc_adder,args=(GST,SVC))

st.write(st.session_state.people_price)




