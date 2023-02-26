"""An AWS Python Pulumi program"""
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pulumi_aws as aws

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='AWS Cost Explorer Dashboard'),
    dcc.Graph(id='aws-graph'),
    dcc.Dropdown(
        id='aws-time-period-dropdown',
        options=[
            {'label': 'Últimos 7 dias', 'value': 'SEVEN_DAYS'},
            {'label': 'Mês atual', 'value': 'MONTH_TO_DATE'},
            {'label': 'Último mês', 'value': 'LAST_MONTH'},
        ],
        value='SEVEN_DAYS'
    ),
    dcc.Dropdown(
        id='aws-granularity-dropdown',
        options=[
            {'label': 'Por hora', 'value': 'HOURLY'},
            {'label': 'Por dia', 'value': 'DAILY'},
        ],
        value='DAILY'
    ),
])

@app.callback(
    Output(component_id='aws-graph', component_property='figure'),
    [Input(component_id='aws-time-period-dropdown', component_property='value'),
     Input(component_id='aws-granularity-dropdown', component_property='value')]
)
def update_aws_graph(time_unit, granularity):
    cost_explorer = aws.get_cost_and_usage( 
        time_period=time_unit,
        granularity=granularity
    )
    data = [
        go.Bar(x=[item["timePeriod"]["start"]], y=[item["total"]["unblendedCost"]], name=item["groupName"])
        for item in cost_explorer["resultsByTime"]
    ]
    layout = go.Layout(title='Custos por serviço', xaxis={'title': 'Período'}, yaxis={'title': 'Custo'})
    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
