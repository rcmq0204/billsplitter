#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 21:21:41 2023

@author: rcmq0204
"""

import streamlit as st
import pandas as pd

st.title('Bill Splitting App')
st.markdown('This app helps to calculate the amount each person has to pay in the bill :moneybag: :money_with_wings:')
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
        st.session_state.people_price[name]=[]

def name_deleter(name:str):
    st.session_state.names.remove(name)
    del st.session_state.people_price[name]

def price_adder(price:float):
    if price<0:
        st.warning(f'Please enter a proper price')
    else:
        st.session_state.prices.append(price)

def even_splitter(people,price,names):
    ppp=price/len(people) #ppp=price per person
    if len(st.session_state.people_price['Food Item'])==0:
        st.session_state.people_price['Food Item'].append(str(1))
    else:
        st.session_state.people_price['Food Item'].append(str(int(st.session_state.people_price['Food Item'][-1])+1))
    st.session_state.people_price['Total'].append(round(price,2))
    for i in names:
        if i not in people:
            st.session_state.people_price[i].append(round(0,2))
        else:
            st.session_state.people_price[i].append(round(ppp,2))



def pct_lst_appender(pct):
    st.session_state.pct_lst.append(pct)



def uneven_sliders(people,i):
    st.session_state.pct_lst=[]
    for name in people:
        pct=st.number_input(name,min_value=0.0,max_value=100.0,step=0.1,format='%.1f',key='pct_splitter_'+str(i),label_visibility='visible')
        i+=1
        pct_lst_appender(pct)
        

def uneven_split(people,pct_lst,price,names):
    if round(sum(pct_lst),1)!=100.0:
        st.warning('Please make sure the sum of the percentages is equal to 100')
    else:
        if len(st.session_state.people_price['Food Item'])==0:
            st.session_state.people_price['Food Item'].append(str(1))
        else:
            st.session_state.people_price['Food Item'].append(str(int(st.session_state.people_price['Food Item'][-1])+1))
        st.session_state.people_price['Total'].append(round(price,2))
        for i in names:
            if i not in people:
                st.session_state.people_price[i].append(round(0,2))
            else:
                pct_price_lst=[]
                for pct in pct_lst:
                    pct_price_lst.append(pct/100*price)
                    idx=people.index(i)
                st.session_state.people_price[i].append(round(pct_price_lst[idx],2))
        st.session_state.pct_lst=[]
  
def gst_svc_adder(GST,SVC,names):
    st.session_state.people_price['Food Item'].extend(['Total','Total++'])
    st.session_state.people_price['Total'].extend([round(sum(st.session_state.people_price['Total']),2),round(sum(st.session_state.people_price['Total'])*(1+SVC/100)*(1+GST/100),2)])
    for i in names:
        st.session_state.people_price[i].extend([round(sum(st.session_state.people_price[i]),2),round(sum(st.session_state.people_price[i])*(1+SVC/100)*(1+GST/100),2)])

def undo_last_step(people_price_dict):
    for key in people_price_dict:
        del people_price_dict[key][-1]

if 'names' not in st.session_state:
    st.session_state.names=[] #list of names

if 'prices' not in st.session_state:
    st.session_state.prices=[] #list of prices

if 'people_price' not in st.session_state:
    st.session_state.people_price={'Food Item':[],'Total':[]}

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

name_df=pd.DataFrame(st.session_state.names,columns=['Names'])
st.dataframe(name_df)
st.write('Ensure that all names are added above')

st.header('Prices and Splits')
price=st.number_input('Enter price of food',format='%.2f')
st.write('The price to be split is $',round(price,2))
st.button('Enter Price',key='price_add',on_click=price_adder,args=(price,))
people=st.multiselect('Select who will split this price',options=st.session_state.names,default=st.session_state.names)
split_choices=st.radio('Even or uneven split',options=['Even','Uneven'],key='choice_split')
if split_choices=='Even':
    st.write('Press the \'Split evenly\' button')
    st.button('Split evenly',key='even_split',on_click=even_splitter,args=(people,price,st.session_state.names))
else:
    st.write('Input percentage split')
    uneven_sliders(people,st.session_state.i)
    st.write('Check the percentages, then click the \'Split unevenly\' button below')
    st.button('Split unevenly',key='uneven_button_splitter',on_click=uneven_split,args=(people,st.session_state.pct_lst,price,st.session_state.names))

st.write('If you made a mistake, click the \'Undo\' button, note this only allows you to undo the latest step')
st.button('Undo',key='Undo_button',on_click=undo_last_step,args=(st.session_state.people_price,))

#once all the prices have been split, need to add gst and svc
st.header('Final amounts')
st.write('Click the \'Compute final amounts\' button to calculate total')
st.write('After clicking the button, note that the \'++\' indicates the price with GST and SVC added')
st.button('Compute final amounts',key='gst_svc_adder',on_click=gst_svc_adder,args=(GST,SVC,st.session_state.names))


people_price_df=pd.DataFrame(st.session_state.people_price)
st.dataframe(people_price_df,use_container_width=True)
