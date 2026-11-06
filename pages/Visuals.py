# This creates the page for displaying data visualizations.

import streamlit as st
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")

import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Game Data Visualizations",
    page_icon="🎮",
    layout="wide"
)

st.title("Game Data Visualizations")

with open("data.json", "r") as file:
    data = json.load(file)

games = data["games"]

st.header("1. Hours Played by Game")

game_names = [game["name"] for game in games]
hours_played = [game["hours_played"] for game in games]

fig, ax = plt.subplots()
ax.bar(game_names, hours_played)
ax.set_title("Total Hours Played by Game")
ax.set_xlabel("Game")
ax.set_ylabel("Hours Played")
ax.tick_params(axis="x", rotation=30)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)


st.header("2. Explore Games by Genre and Rating")

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = "All"

if "minimum_rating" not in st.session_state:
    st.session_state.minimum_rating = 1


genres = sorted(set(game["genre"] for game in games))

genre_options = ["All"] + genres

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = "All"

if st.session_state.selected_genre in genre_options:
    default_index = genre_options.index(st.session_state.selected_genre)
else:
    default_index = 0

selected_genre = st.selectbox(
    "Choose a genre",
    genre_options,
    index=default_index,
    key="genre_input"
)

minimum_rating = st.slider(
    "Minimum rating",
    min_value=1,
    max_value=10,
    value=st.session_state.minimum_rating,
    key="rating_input"
)

st.session_state.selected_genre = selected_genre
st.session_state.minimum_rating = minimum_rating


filtered_games = [
    game for game in games
    if (selected_genre == "All" or game["genre"] == selected_genre)
    and game["rating"] >= minimum_rating
]

if filtered_games:
    fig_dynamic = px.scatter(
        filtered_games,
        x="hours_played",
        y="rating",
        color="genre",
        hover_name="name",
        title="Game Ratings vs. Hours Played",
        labels={
            "hours_played": "Hours Played",
            "rating": "Rating (1–10)",
            "genre": "Genre"
        }                       
    )

    st.plotly_chart(fig_dynamic, use_container_width=True)
else:
    st.warning("No games match your selected filters.")



# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

st.divider()
st.header("Student Survey Data Visualizations")

# Read the CSV file
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    df = pd.read_csv("data.csv")

    # Make sure the CSV contains the required columns
    if "Category" in df.columns and "Value" in df.columns:

        # Convert values into numbers
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

        # Remove invalid or empty rows
        df = df.dropna(subset=["Category", "Value"])

        if not df.empty:
            # GRAPH 3: STATIC BAR CHART

            st.subheader("3. Average Value by Category")

            st.write(
                "This chart displays the average value "
                "submitted for each category."
            )

            # Calculate average value for each category
            average_values = df.groupby("Category")["Value"].mean()

            # Create Matplotlib bar chart
            fig, ax = plt.subplots()

            ax.bar(
                average_values.index,
                average_values.values
            )

            ax.set_title("Average Value by Category")
            ax.set_xlabel("Category")
            ax.set_ylabel("Average Value")

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            # GRAPH 4: DYNAMIC SCATTER PLOT

            st.subheader("4. Explore Survey Data")

            st.write(
                "Use the slider to filter responses "
                "based on their minimum value."
            )

            # Initialize session state
            if "minimum_value" not in st.session_state:
                st.session_state.minimum_value = 0

            # Set slider range based on CSV data
            min_value = min(0, int(df["Value"].min()))
            max_value = max(10, int(df["Value"].max()) + 1)

            # User interaction
            minimum_value = st.slider(
                "Select minimum value",
                min_value=min_value,
                max_value=max_value,
                key="minimum_value"
            )

            # Filter the original CSV data
            filtered_df = df[df["Value"] >= minimum_value].copy()

            # Give each response a number
            filtered_df["Response"] = range(1, len(filtered_df) + 1)

            st.write(
                f"Number of responses displayed: {len(filtered_df)}"
            )

            # Create dynamic Plotly scatter plot
            if not filtered_df.empty:

                fig_dynamic = px.scatter(
                    filtered_df,
                    x="Response",
                    y="Value",
                    color="Category",
                    title="Survey Responses by Category",
                    labels={
                        "Response": "Response Number",
                        "Value": "Submitted Value",
                        "Category": "Category"
                    }
                )

                st.plotly_chart(
                    fig_dynamic,
                    use_container_width=True
                )

            else:
                st.warning("No responses match your selected filter.")

        else:
            st.warning("There is no valid numerical survey data yet.")

    else:
        st.error(
            "Your CSV file must contain Category and Value columns."
        )

else:
    st.warning(
        "No survey data found. Please submit some responses "
        "using the Survey page first."
    )
