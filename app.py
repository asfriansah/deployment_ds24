import streamlit as st
import pickle

def main():
    background = """<div style = 'background-colour:black'; padding:13px>
                    <h1 style = 'colour:white'>Loan Eligibility Prediction App</h1>
                    </div>"""
    st.markdown(background, unsafe_allow_html=True)

    left, right = st.columns((2,2))
    gender = left.selectbox('Gender',('Male','Female'))
    married = left.selectbox('Married',('Yes','No'))
    dependent = left.selectbox('Dependents',('None','One','Two','Three'))
    education = left.selectbox('Education',('Graduate','Not Graduate'))
    self_employed = left.selectbox('Self-Employed',('Yes','No'))
    application_income = right.number_input('Application Income')
    coapplication_income = right.number_input('Coapplication Income')
    loan_amount = right.number_input('Loan Amount')
    loan_amount_term = right.number_input('Loan Amount Term')
    credit_history= right.number_input('Credit History',0.0,1.0)
    property_area = left.selectbox('Property Area',('Semiurban','Urban','Rural'))
    button = st.button('Predict')

    if button:
        result = predict(gender,married,dependent,education,self_employed,application_income,
                         coapplication_income,loan_amount,loan_amount_term,credit_history,property_area)
        st.success(f'You Are {result} for the loan')

    st.markdown("""<style>
                    [data-testid=stSidebar] {
                        background-color: #b2cf99;
                    }
                </style>
                """, unsafe_allow_html=True)
    with st.sidebar:
        
        st.subheader('About')
        st.markdown('<div style="text-align: justify;">This is an application for predicting whether a customer is eligible to get a loan or not. Predictions using the Random Forest algorithm model with an accuracy of 82.5%</div>', unsafe_allow_html=True)
        st.sidebar.image('https://cdn-icons-png.flaticon.com/512/2660/2660135.png')
        title_alignment = """<h4 style = 'text-align: center'>created 2023 by andri asfriansah</h4>"""
                                
        st.markdown(title_alignment, unsafe_allow_html=True)
        #st.markdown('created by andri asfriansah',)

with open('model/Random_Forest_model(1).pkl','rb') as file:
    RF_Model = pickle.load(file)

def predict(gender,married,dependent,education,self_employed,application_income,
                         coapplication_income,loan_amount,loan_amount_term,credit_history,property_area):
    gen = 0 if gender == 'Male' else 1
    mar = 0 if married == 'Yes' else 1
    dep = float(0 if dependent == 'None' else 1 if dependent == 'One' else 2 if dependent == 'Two' else 3)
    edu = 0 if education == 'Graduate' else 1
    sem = 0 if self_employed == 'Yes' else 1
    pro = 0 if property_area == 'Semiurban' else 1 if property_area == 'Urban' else 2
    lam = loan_amount / 1000
    cap = coapplication_income /1000

    prediction = RF_Model.predict([[gen,mar,dep,edu,sem,application_income,cap,lam,
                                   loan_amount_term,credit_history,pro]])
    verdict = 'Not Eligible' if prediction == 0 else 'Eligible'
    return verdict


if __name__ == "__main__":
    main()

