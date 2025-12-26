import streamlit as st
import pickle
import numpy as np
import pandas as pd


def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    return model


model = load_model()


def strToIntBool(s):
    if s == 'True':
        return 1
    else:
        return 0


def show_predict_page():
    st.title("سامانه تشخیص تقلب در تراکنش‌های کارت اعتباری")
    st.subheader("پروژه تشخیص تقلب ")
    
    st.write("### لطفاً اطلاعات تراکنش را وارد کنید تا مشخص شود آیا تراکنش مشکوک است یا خیر")
    
    # Input fields
    distance_from_home = st.number_input('فاصله از محل سکونت ')
    distance_from_last_transaction = st.number_input('فاصله از آخرین تراکنش ')
    ratio_to_median_purchase_price = st.number_input('نسبت مبلغ خرید به میانگین خرید')
    
    repeat_retailer = st.radio('خرید تکراری از همین فروشنده', ["False", "True"])
    used_chip = st.radio('استفاده از چیپ کارت', ["False", "True"])
    used_pin_number = st.radio('استفاده از رمز کارت (PIN)', ["False", "True"])
    online_order = st.radio('سفارش آنلاین', ["False", "True"])


    input_dict = {
        'distance_from_home': distance_from_home,
        'distance_from_last_transaction': distance_from_last_transaction,
        'ratio_to_median_purchase_price': ratio_to_median_purchase_price,
        'repeat_retailer': strToIntBool(repeat_retailer),
        'used_chip': strToIntBool(used_chip),
        'used_pin_number': strToIntBool(used_pin_number),
        'online_order': strToIntBool(online_order)
    }

    # Convert inputs to DataFrame
    input_df = pd.DataFrame([input_dict])

    if st.button("پیش‌بینی تراکنش"):
        prediction = model.predict(input_df)

        if prediction[0]:
            st.error('🚨 این تراکنش مشکوک است')
        else:
            st.success('✅ این تراکنش سالم و معتبر است')
