# Import required libraries
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get unique launch sites
launch_sites = spacex_df["Launch Site"].unique()
launch_sites = np.insert(launch_sites,0,["All Sites"])# Include "ALL" option

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                            id='launch-site-dropdown',  # Unique ID for the dropdown
                                            options=[{"label": site, "value": site} for site in launch_sites],
                                            value="ALL",  # Default selection
                                            placeholder="Select Launch Site",
                                            searchable=True  # Default value
                                            ),
                                dcc.Graph(id="success-pie-chart"),
                                
                                html.Label("Payload range (Kg):", style={"textAlign": "left"}),
                                    # RangeSlider for payload mass
                                dcc.RangeSlider(id="payload-slider",
                                    min=spacex_df["Payload Mass (kg)"].min(),
                                    max=spacex_df["Payload Mass (kg)"].max(),
                                    step=1000,
                                    value=[spacex_df["Payload Mass (kg)"].min(), spacex_df["Payload Mass (kg)"].max()],
                                    marks={i: str(i) for i in range(0, 10000, 1000)},
                                                ),

                                # Scatter plot to show correlation between payload and launch success
                                dcc.Graph(id="success-payload-scatter-chart"),
                                ]
                    )
html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
#html.Div(dcc.Graph(id='success-pie-chart')),
#html.Br(),

# Callback for pie chart (total successful launches by sites)
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='launch-site-dropdown', component_property='value'))

def update_pie_chart(selected_site):
    if selected_site == "All Sites":
        fig_pie = px.pie(spacex_df, names="Launch Site", values="class", title="Total Successful Launches by Sites")
    else:
        site_data = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig_pie = px.pie(site_data, names="class", title=f"Total Success Launches for {selected_site}")
    return fig_pie

# Callback for scatter plot (correlation between payload and launch success)
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("launch-site-dropdown", "value"),
     Input("payload-slider", "value")]
)
def get_scatter_chart(entered_site, payload):
    df_filtered = spacex_df.loc[(spacex_df["Payload Mass (kg)"] >= payload[0]) & (spacex_df["Payload Mass (kg)"] <= payload[1])]
    if entered_site == "All Sites":
        fig = px.scatter(df_filtered, x="Payload Mass (kg)", y="class", color="Booster Version", hover_data=["Booster Version"])
    else:
        df_site_filtered = df_filtered.loc[df_filtered["Launch Site"] == entered_site]
        fig = px.scatter(df_site_filtered, x="Payload Mass (kg)", y="class", color="Booster Version", hover_data=["Booster Version"])
    return fig


                                # TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, marks={0: '0', 100: '100'}, value=[min_value, max_value])

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
#html.Div(dcc.Graph(id='success-payload-scatter-chart')),


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
