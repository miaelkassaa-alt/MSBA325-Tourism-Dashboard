
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("MSBA325.csv")

st.title("Tourism in Lebanon")

st.write(
    "Explore how tourism facilities differ among Lebanese towns "
    "at different levels of tourism activity."
)

tourism_range = st.slider(
    "Select Tourism Index range:",
    min_value=0,
    max_value=10,
    value=(0, 10)
)

# Filter data according to selected Tourism Index range
filtered_df = df[
    (df["Tourism Index"] >= tourism_range[0]) &
    (df["Tourism Index"] <= tourism_range[1])
]

st.subheader("Tourism Facilities by Town")

facility_data = filtered_df.groupby("Town")[
    ["Total number of hotels",
     "Total number of cafes",
     "Total number of guest houses",
     "Total number of restaurants"]
].sum().reset_index()

facility_data["Total Facilities"] = (
    facility_data["Total number of hotels"] +
    facility_data["Total number of cafes"] +
    facility_data["Total number of guest houses"] +
    facility_data["Total number of restaurants"]
)

facility_data = facility_data.sort_values(
    "Total Facilities", ascending=False
).head(10)

fig1 = px.bar(
    facility_data,
    x="Town",
    y="Total Facilities",
    title="Top 10 Towns by Total Tourism Facilities"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Tourism Facilities Distribution")

treemap_data = filtered_df.groupby("Town").agg({
    "Total number of hotels": "sum",
    "Total number of cafes": "sum",
    "Total number of guest houses": "sum",
    "Total number of restaurants": "sum",
    "Tourism Index": "mean"
}).reset_index()

treemap_data["Total Facilities"] = (
    treemap_data["Total number of hotels"] +
    treemap_data["Total number of cafes"] +
    treemap_data["Total number of guest houses"] +
    treemap_data["Total number of restaurants"]
)

treemap_data = treemap_data[treemap_data["Total Facilities"] > 0]

fig2 = px.treemap(
    treemap_data,
    path=["Town"],
    values="Total Facilities",
    color="Tourism Index",
    hover_data=["Tourism Index"],
    title="Distribution of Tourism Facilities Across Lebanese Towns"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Explore a Specific Town")

town_options = ["All Towns"] + sorted(filtered_df["Town"].dropna().unique().tolist())

selected_town = st.selectbox(
    "Select a town:",
    town_options
)

if selected_town == "All Towns":
    selected_df = filtered_df
else:
    selected_df = filtered_df[filtered_df["Town"] == selected_town]

st.write("Selected town:", selected_town)

if selected_town != "All Towns":
    town_info = selected_df.groupby("Town").agg({
        "Total number of hotels": "sum",
        "Total number of cafes": "sum",
        "Total number of guest houses": "sum",
        "Total number of restaurants": "sum"
    }).reset_index()

    town_long = town_info.melt(
        id_vars="Town",
        var_name="Facility Type",
        value_name="Number"
    )

    fig3 = px.bar(
        town_long,
        x="Facility Type",
        y="Number",
        title=f"Tourism Facilities in {selected_town}"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Key Insights")

st.markdown("""
**1. Ghobairi has the highest concentration of tourism facilities.**  
Ghobairi has 177 facilities in total, largely driven by 90 cafés and 83 restaurants.

**2. A high Tourism Index does not necessarily mean more facilities.**  
Among towns with a Tourism Index of 10, total facilities vary considerably, from 7 in Vidar to 108 in Zahleh El-Maallaqa.
""")

st.subheader("Interaction Design")

with st.expander("Why use a Tourism Index range slider?"):
    st.write("""
    The slider helps users answer: How do tourism facilities differ among towns
    at different levels of tourism activity? A range slider was chosen instead
    of a dropdown because the Tourism Index is an ordered numerical variable,
    and users may want to explore several index values at once. This interaction
    focuses attention and reduces clutter by displaying only towns within the
    selected range.
    """)

with st.expander("Why use a town dropdown?"):
    st.write("""
    The dropdown helps users answer: What is the mix of tourism facilities in a
    specific town within the selected Tourism Index range? A dropdown was chosen
    instead of displaying all towns at once because there are many towns in the
    dataset. It reduces clutter and allows the user to focus on one town. The
    dropdown is linked to the Tourism Index slider because its available towns
    come from the data remaining after the index filter, creating a broad-to-specific
    drill-down.
    """)
