from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd

data = {
    'class': ['Math', 'Science', 'History', 'English'],
    'attendance': [0.92, 0.85, 0.88, 0.95],
    'concentration': [0.75, 0.68, 0.80, 0.90]
}
df = pd.DataFrame(data)
df['attendance_pct'] = df['attendance'].clip(upper=1) * 100
df['concentration_pct'] = df['concentration'].clip(upper=1) * 100

app = Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])
app.title = 'Beyond Learning'

options = [{'label': cls, 'value': cls} for cls in sorted(df['class'])]

app.layout = html.Div(
    className='container',
    children=[
        html.H1('Beyond Learning', className='my-4 text-center'),
        dcc.Dropdown(id='class-dropdown', options=options, value=options[0]['value'], className='mb-4'),
        html.Div(id='metrics-text', className='mb-4'),
        html.Div(
            className='row',
            children=[
                html.Div(dcc.Graph(id='attendance-graph'), className='col-md-6'),
                html.Div(dcc.Graph(id='concentration-graph'), className='col-md-6'),
            ],
        ),
        html.H2('All Classes Overview', className='my-4'),
        dash_table.DataTable(
            id='metrics-table',
            columns=[
                {'name': 'Class', 'id': 'class'},
                {'name': 'Attendance (%)', 'id': 'attendance_pct', 'type': 'numeric', 'format': {'specifier': '.1f'}},
                {'name': 'Concentration (%)', 'id': 'concentration_pct', 'type': 'numeric', 'format': {'specifier': '.1f'}}
            ],
            data=df.to_dict('records'),
            sort_action='native',
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '5px'},
            style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold'}
        ),
    ]
)

@app.callback(
    Output('metrics-text', 'children'),
    Output('attendance-graph', 'figure'),
    Output('concentration-graph', 'figure'),
    Input('class-dropdown', 'value')
)
def update_metrics(selected):
    row = df.loc[df['class'] == selected].squeeze()
    att = row['attendance_pct']
    conc = row['concentration_pct']
    metrics = [
        html.P(f"Attendance: {att:.1f}%", className='lead'),
        html.P(f"Concentration: {conc:.1f}%", className='lead')
    ]
    attendance_fig = {
        'data': [{'x': [selected], 'y': [att], 'type': 'bar'}],
        'layout': {'title': 'Attendance (%)', 'yaxis': {'range': [0, 100]}}
    }
    concentration_fig = {
        'data': [{'x': [selected], 'y': [conc], 'type': 'bar'}],
        'layout': {'title': 'Concentration (%)', 'yaxis': {'range': [0, 100]}}
    }
    return metrics, attendance_fig, concentration_fig

if __name__ == '__main__':
    app.run(debug=False)

