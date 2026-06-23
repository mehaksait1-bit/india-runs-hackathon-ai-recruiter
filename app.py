import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Recruiter",
    layout="wide"
)

st.title("🤖 AI Recruiter System")

st.write(
    "Candidate Ranking using Skills, Experience and Recruiter Signals"
)

df = pd.read_csv("submission.csv")

st.subheader("Top Candidates")

st.dataframe(df)

candidate = st.text_input(
    "Search Candidate ID"
)

if candidate:

    result = df[
        df["candidate_id"]
        .str.contains(
            candidate,
            case=False
        )
    ]

    st.dataframe(result)

st.subheader(
    "Top 20 Candidate Scores"
)

chart_df = (
    df.head(20)
      .set_index(
          "candidate_id"
      )
)

st.bar_chart(
    chart_df["score"]
)