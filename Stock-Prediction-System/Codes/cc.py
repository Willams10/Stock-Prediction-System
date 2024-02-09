import streamlit as st
from forex_python.converter import CurrencyRates

def app():
    def real_time_currency_conversion(amount, from_currency, to_currency):
        c = CurrencyRates()
        converted_amount = c.convert(from_currency, to_currency, amount)
        return converted_amount


    def perform_conversion():
        if amount > 0:
            result = real_time_currency_conversion(amount, from_currency, to_currency)
            st.session_state.converted_amount = f'{result:.2f} {to_currency}'
        else:
            st.error("Please enter a valid amount greater than 0")

    def get_currency_codes():
        c = CurrencyRates()
        currency_codes = list(c.get_rates('').keys())  
        return currency_codes


    st.title('Currency Converter')

    currency_codes = get_currency_codes()

    col1, col2 = st.columns(2)

    default_from_currency = 'USD' if 'USD' in currency_codes else currency_codes[0]
    default_to_currency = 'EUR' if 'EUR' in currency_codes else currency_codes[1]

    if 'converted_amount' not in st.session_state:
        st.session_state.converted_amount = ''

    with col1: 
        st.subheader('From Currency')
        from_currency = st.selectbox('Select the currency you want to convert from:', currency_codes, index=currency_codes.index(default_from_currency))
        amount = st.number_input('Enter the amount you want to convert:', min_value=0.0, format="%.2f")

    with col2:  
        st.subheader('To Currency')
        to_currency = st.selectbox('Select the currency you want to convert to:', currency_codes, index=currency_codes.index(default_to_currency))
        converted_amount_field = st.text_input('Converted amount:', value=st.session_state.converted_amount, disabled=True)


    if st.button('Convert', on_click=perform_conversion):
        pass


    if st.button('Clear'):
        st.session_state.converted_amount = ''
        st.session_state.amount = 0.0
        st.session_state.from_currency = default_from_currency
        st.session_state.to_currency = default_to_currency

