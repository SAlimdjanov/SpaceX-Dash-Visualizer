"""
app.py

SpaceX Dash Visualizer App

"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px


def process_data():
    """Processes the content in the dataset

    Returns:
        tuple (pd.DataFrame, float, float): Launch data in a DataFrame, max payload mass, min
        payload mass
    """
    df = pd.read_csv("./assets/spacex_launch_data.csv")

    df["Payload Mass (kg)"] = df["Payload Mass (kg)"].str.replace("~", "")
    df["Payload Mass (kg)"] = df["Payload Mass (kg)"].replace("Classified", np.inf)
    df["Payload Mass (kg)"].fillna(-np.inf)
    df["Payload Mass (kg)"] = df["Payload Mass (kg)"].str.replace(",", "")
    df["Payload Mass (kg)"] = df["Payload Mass (kg)"].astype(float)

    maximum = df["Payload Mass (kg)"].max()
    minimum = df["Payload Mass (kg)"].min()

    return df, maximum, minimum


# Process csv data

spacex_df, max_payload, min_payload = process_data()

# Dash Application

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"font-family": "Arial"},
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # Dropdown list to select launch site
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
            ],
            value="ALL",
            placeholder="place holder here",
            searchable=True,
        ),
        html.Br(),
        # Pie chart
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload Mass Range (kg):"),
        # Slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={0: "0", 10000: "10000"},
            tooltip={"placement": "bottom", "always_visible": True},
            value=[min_payload, max_payload],
        ),
        # Scatter chart
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ],
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    """Generates a plotly pie chart of showing

    Args:
        entered_site (str): launch site from drop-down menu

    Returns:
        plotly figure: pie chart with data specified in drop-down menu

    """
    if entered_site == "ALL":
        fig = px.pie(
            spacex_df,
            names="Mission Outcome",
            title="Success Rate for All Launch Sites",
        )
        return fig

    filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
    fig = px.pie(
        filtered_df,
        names="Mission Outcome",
        title=f"Total Success Launches for Site: {entered_site}",
    )
    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(entered_site, slider):
    """Generates a plotly scatter chart given the launch site and payload range slider

    Args:
        entered_site (str): Launch site from drop-down menu
        slider (list): Slider values

    Returns:
        plotly figure: Scatter plot with data specified in range slider
    """
    filtered_df = spacex_df[
        (slider[0] <= spacex_df["Payload Mass (kg)"])
        & (spacex_df["Payload Mass (kg)"] <= slider[1])
    ]

    if entered_site != "ALL":
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]

    return px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="Mission Outcome",
        color="Mission Outcome",
        title=f"Launch Outcomes for: {entered_site if entered_site != 'ALL' else 'All Sites'}",
    )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=9000)
