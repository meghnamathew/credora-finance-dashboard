import os, sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(ROOT,"credora_finance.db")
SCORED=os.path.join(ROOT,"scored_applications.csv")
st.set_page_config(page_title="Credora Finance Risk Analytics",layout="wide")
st.title("Credora Finance — Credit Risk Analytics Dashboard")
st.caption("Internship project prototype | Decision support only; not an automated lending decision.")
@st.cache_data
def load_data():
    con=sqlite3.connect(DB)
    apps=pd.read_sql_query("SELECT * FROM loan_applications",con)
    cust=pd.read_sql_query("SELECT customer_id, age, annual_income, city, state, employment_type, kyc_status FROM customers",con)
    credit=pd.read_sql_query("SELECT customer_id, credit_score, credit_utilization_ratio, num_late_payments_90d, num_defaults_prior, total_outstanding_debt FROM credit_history",con)
    txn=pd.read_sql_query("SELECT * FROM transactions",con)
    con.close()
    scored=pd.read_csv(SCORED)
    return apps,cust,credit,txn,scored
apps,cust,credit,txn,scored=load_data()
apps=apps.merge(cust,on="customer_id",how="left").merge(credit,on="customer_id",how="left")
scored=scored.merge(cust,on="customer_id",how="left")
region=st.sidebar.selectbox("State",["All"]+sorted(scored["state"].dropna().unique().tolist()))
risk=st.sidebar.multiselect("Risk category",["Low","Medium","High"],default=["Low","Medium","High"])
loan_types=st.sidebar.multiselect("Loan type",sorted(scored["loan_type"].dropna().unique().tolist()),default=sorted(scored["loan_type"].dropna().unique().tolist()))
view=scored[scored["risk_category"].isin(risk)&scored["loan_type"].isin(loan_types)]
if region!="All": view=view[view["state"]==region]
k1,k2,k3,k4=st.columns(4)
k1.metric("Total applications",f"{len(apps):,}")
k2.metric("Approval rate",f"{(apps.approval_status=='Approved').mean():.1%}")
known=apps[apps.loan_default.notna()]
k3.metric("Observed default rate",f"{known.loan_default.mean():.1%}")
k4.metric("Average credit score",f"{apps.credit_score.mean():.0f}")
c1,c2=st.columns(2)
with c1:
    st.subheader("Application decision status")
    st.plotly_chart(px.bar(apps["approval_status"].value_counts().rename_axis("status").reset_index(name="count"),x="status",y="count"),use_container_width=True)
with c2:
    st.subheader("Observed default rate by loan type")
    d=known.groupby("loan_type",as_index=False).loan_default.mean()
    d["default_rate_pct"]=d.loan_default*100
    st.plotly_chart(px.bar(d,x="loan_type",y="default_rate_pct"),use_container_width=True)
c3,c4=st.columns(2)
with c3:
    st.subheader("Monthly application volume")
    m=apps.assign(month=pd.to_datetime(apps.application_date).dt.to_period("M").astype(str)).groupby("month",as_index=False).size()
    st.plotly_chart(px.line(m,x="month",y="size"),use_container_width=True)
with c4:
    st.subheader("Risk category distribution (model estimates)")
    st.plotly_chart(px.pie(view,names="risk_category",title="Filtered scored applications"),use_container_width=True)
st.subheader("Geographic portfolio view")
geo=view.groupby(["state","city"],as_index=False).agg(applications=("application_id","count"),mean_risk=("risk_score","mean"))
st.plotly_chart(px.scatter(geo,x="applications",y="mean_risk",size="applications",hover_name="city",color="state"),use_container_width=True)
st.subheader("High-risk watchlist")
watch=view[view.risk_category=="High"].sort_values("predicted_default_probability",ascending=False)
st.dataframe(watch[["application_id","loan_type","requested_amount","predicted_default_probability","risk_score","risk_category","city","state"]].head(500),use_container_width=True)
st.download_button("Download filtered scored applications",view[["application_id","loan_type","requested_amount","predicted_default_probability","risk_score","risk_category","city","state"]].to_csv(index=False),"credora_filtered_scores.csv","text/csv")
st.info("Risk scores are model estimates on the supplied sample. Validate thresholds, fairness and business impact before any real lending use.")
