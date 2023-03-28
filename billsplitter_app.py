#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 21:21:41 2023

@author: rcmq0204
"""

import streamlit as st

st.title('Bill Splitting App')
st.markdown('This app helps to calculate the amount each person has to pay in the bill :)')
st.header('GST and/or SVC')
st.write('Click the following checkboxes if there is GST and/or SVC')
if st.checkbox('GST'):
    GST=st.number_input(f'Enter the GST in % here (if GST is 8%, type 8)')
    st.write('The GST is ',GST,'%')
else:
    GST=0
    st.write('The GST is ',GST,'%')

if st.checkbox('SVC'):
    SVC=st.number_input(f'Enter the SVC in % here (if SVC is 10%, type 10)')
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

def even_splitter(people:list,price:float):
    ppp=price/len(people) #ppp=price per person
    for i in people:
        st.session_state.people_price[i]+=ppp


def pct_lst_appender(pct):
    st.session_state.pct_lst.append(pct)



def uneven_sliders(people,i):
    st.session_state.pct_lst=[]
    for name in people:
        pct=st.number_input(name,min_value=0.0,max_value=100.0,step=0.1,format='%.1f',key='pct_splitter_'+str(i),label_visibility='visible')
        i+=1
        pct_lst_appender(pct)
        

def uneven_split(people,pct_lst,price):
    if round(sum(pct_lst),1)!=100.0:
        st.warning('Please make sure the sum of the percentages is equal to 100')
    else:
        pct_price_lst=[]
        for pct in pct_lst:
            pct_price_lst.append(pct/100*price)
        for i in people:
            idx=people.index(i)
            st.session_state.people_price[i]+=pct_price_lst[idx]
        st.session_state.pct_lst=[]
  
def gst_svc_adder(GST:float,SVC:float):
    for key in st.session_state.people_price:
        st.session_state.people_price[key]=round(st.session_state.people_price[key]*(1+SVC/100)*(1+GST/100),2)

if 'names' not in st.session_state:
    st.session_state.names=[] #list of names

if 'prices' not in st.session_state:
    st.session_state.prices=[] #list of prices

if 'people_price' not in st.session_state:
    st.session_state.people_price={}

if 'pct_split' not in st.session_state:
    st.session_state.pct_split=[]

if 'i' not in st.session_state:
    st.session_state.i=0

if 'pct_lst' not in st.session_state:
    st.session_state.pct_lst=[]

st.header('Names')
name=st.text_input('Enter name here (one at a time)',key='new_name')
st.button('Add name',key='button_add_name',on_click=name_adder,args=(name,))

name_del=st.selectbox('If you wish to delete a name, select the name then press delete',st.session_state.names)
st.button('Delete',key='name_del',on_click=name_deleter,args=(name_del,))
    
st.write(st.session_state.names)
st.write('Ensure that all names are added above')

st.header('Prices and Splits')
price=st.number_input('Enter price of food',format='%.2f')
st.button('Enter Price',key='price_add',on_click=price_adder,args=(price,))
people=st.multiselect('Select who will split this price',options=st.session_state.names,default=st.session_state.names)
split_choices=st.radio('Even or uneven split',options=['Even','Uneven'],key='choice_split')
if split_choices=='Even':
    st.write('Press the \'Split evenly\' button')
    st.button('Split evenly',key='even_split',on_click=even_splitter,args=(people,price))
else:
    st.write('Input percentage split')
    uneven_sliders(people,st.session_state.i)
    st.write('The price to be split is $',price)
    st.write('Check the percentages, then click the \'Split unevenly\' button below')
    st.button('Split unevenly',key='uneven_button_splitter',on_click=uneven_split,args=(people,st.session_state.pct_lst,price))

    
#once all the prices have been split, need to add gst and svc
st.header('Final amounts')
st.write('Click the button below to include the GST and SVC')
st.button('Compute final amounts',key='gst_svc_adder',on_click=gst_svc_adder,args=(GST,SVC))

st.write(st.session_state.people_price)