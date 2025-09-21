import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

# CPT for Study Abroad Probability
def get_study_abroad_prob(academic, language, country, field, confidence, decision_style, motivation='High'):
    base_table = {
        ('High', 'Excellent'): 0.85,
        ('Average', 'Moderate'): 0.60,
        ('Low', 'Poor'): 0.30
    }
    field_modifier = {
        'STEM': 1.0, 'Arts': 0.9, 'Business': 0.95, 'Social Sciences': 0.85, 'Health': 0.9
    }
    country_modifier = {
        'Germany': 1.0, 'UK': 0.95, 'Netherlands': 0.9, 'USA': 0.85
    }
    prospera_modifier = {
        'confidence': {'High': 1.0, 'Moderate': 0.85, 'Low': 0.7},
        'decision_style': {'Analytical': 1.0, 'Mixed': 0.9, 'Intuitive': 0.85},
        'motivation': {'High': 1.0, 'Medium': 0.9, 'Low': 0.8}
    }

    base = base_table.get((academic, language), 0.5)
    prob = base * field_modifier[field] * country_modifier[country]
    prob *= prospera_modifier['confidence'][confidence]
    prob *= prospera_modifier['decision_style'][decision_style]
    prob *= prospera_modifier['motivation'][motivation]
    return round(prob, 2)

# Mapping scores
confidence_scores = {'High': 0.9, 'Moderate': 0.6, 'Low': 0.3}
interest_scores = {'STEM': 0.9, 'Arts': 0.8, 'Business': 0.85, 'Social Sciences': 0.75, 'Health': 0.8}

app.layout = html.Div([
    html.H2("Study Abroad Decision Network + Prospera"),

    html.Label("Academic Performance"),
    dcc.RadioItems(['High', 'Average', 'Low'], 'High', id='academic'),

    html.Label("Language Proficiency"),
    dcc.RadioItems(['Excellent', 'Moderate', 'Poor'], 'Excellent', id='language'),

    html.Label("Target Country"),
    dcc.RadioItems(['Germany', 'UK', 'Netherlands', 'USA'], 'Germany', id='country'),

    html.Label("Field of Study"),
    dcc.RadioItems(list(interest_scores.keys()), 'STEM', id='field'),

    html.Label("Career Interest Area (Prospera)"),
    dcc.RadioItems(list(interest_scores.keys()), 'STEM', id='career_interest'),

    html.Label("Confidence in Field (Prospera)"),
    dcc.RadioItems(list(confidence_scores.keys()), 'High', id='confidence'),

    html.Label("Decision-Making Style (Prospera)"),
    dcc.RadioItems(['Analytical', 'Intuitive', 'Mixed'], 'Analytical', id='decision_style'),

    html.Br(),
    html.Div(id='output'),
    dcc.Graph(id='match_graph')
], style={'padding': '16px', 'fontFamily': 'Arial', 'fontSize': '12px'})


@app.callback(
    Output('output', 'children'),
    Output('match_graph', 'figure'),
    Input('academic', 'value'),
    Input('language', 'value'),
    Input('country', 'value'),
    Input('field', 'value'),
    Input('career_interest', 'value'),
    Input('confidence', 'value'),
    Input('decision_style', 'value')
)
def update_output(academic, language, country, field, career_interest, confidence, decision_style):
    prob = get_study_abroad_prob(academic, language, country, field, confidence, decision_style)

    # Match score between interest and confidence
    match_score = round(confidence_scores[confidence] * interest_scores[career_interest] * 100, 2)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_score,
        title={'text': "Съвпадение между интерес и увереност"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': match_score
            }
        }
    ))

    suggestions = []
    if confidence == 'Low' and interest_scores[career_interest] >= 0.8:
        suggestions = [field for field, score in interest_scores.items()
                       if score >= 0.8 and field != career_interest]

    suggestion_text = html.Div([
        html.P(f"Вероятност за обучение в чужбина: {prob}/1"),
        html.P(f"Съвпадение между интерес и увереност: {match_score}/100"),
        html.P(f"Стил на вземане на решения: {decision_style}"),
        html.P("Предложени алтернативни сфери:" if suggestions else "Няма нужда от алтернативни предложения."),
        html.Ul([html.Li(field) for field in suggestions]) if suggestions else None
    ])

    return suggestion_text, fig


if __name__ == '__main__':
    app.run(debug=False)
app = dash.Dash(__name__)
server = app.server  # ← това е важно за Render
