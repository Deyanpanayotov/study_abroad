import dash
from dash import html, dcc, Input, Output

app = dash.Dash(__name__)

# CPT for Study Abroad Probability
def get_study_abroad_prob(academic, language, country, field):
    base_table = {
        ('High', 'Excellent'): 0.85,
        ('Average', 'Moderate'): 0.60,
        ('Low', 'Poor'): 0.30
    }
    field_modifier = {
        'STEM': 1.0,
        'Arts': 0.9,
        'Business': 0.95,
        'Social Sciences': 0.85,
        'Health': 0.9
    }
    country_modifier = {
        'Germany': 1.0,
        'UK': 0.95,
        'Netherlands': 0.9,
        'USA': 0.85
    }
    base = base_table.get((academic, language), 0.5)
    return round(base * field_modifier[field] * country_modifier[country], 2)

# Utility function with range
def compute_utility_range(prob, finance, support, arts, portfolio, visa, tuition, work_rights,
                          adaptability, culture, digital, school_support, peer):
    def score(val, scale): return scale.get(val, 0.6)

    scales = {
        'finance': {'Stable': 0.9, 'Volatile': 0.6, 'In Debt': 0.3},
        'support': {'Strong': 0.9, 'Average': 0.6, 'None': 0.3},
        'arts': {'High': 0.9, 'Moderate': 0.6, 'Low': 0.3},
        'portfolio': {'Strong': 0.9, 'Average': 0.6, 'Weak': 0.3},
        'visa': {'Supportive': 0.9, 'Neutral': 0.6, 'Restrictive': 0.3},
        'tuition': {'Low': 0.9, 'Moderate': 0.6, 'High': 0.3},
        'work_rights': {'Generous': 0.9, 'Limited': 0.6, 'None': 0.3},
        'adaptability': {'High': 0.9, 'Medium': 0.6, 'Low': 0.3},
        'culture': {'Open': 0.9, 'Neutral': 0.6, 'Reserved': 0.3},
        'digital': {'Advanced': 0.9, 'Basic': 0.6, 'Limited': 0.3},
        'school_support': {'Strong': 0.9, 'Average': 0.6, 'Weak': 0.3},
        'peer': {'Encouraging': 0.9, 'Neutral': 0.6, 'Discouraging': 0.3}
    }

    weights = {
        'prob': 0.3, 'finance': 0.07, 'support': 0.07, 'arts': 0.05, 'portfolio': 0.05,
        'visa': 0.05, 'tuition': 0.05, 'work_rights': 0.05, 'adaptability': 0.05,
        'culture': 0.05, 'digital': 0.05, 'school_support': 0.06, 'peer': 0.05
    }

    expected = (
        prob * 100 * weights['prob'] +
        sum(score(val, scales[key]) * 100 * weights[key]
            for key, val in {
                'finance': finance, 'support': support, 'arts': arts, 'portfolio': portfolio,
                'visa': visa, 'tuition': tuition, 'work_rights': work_rights,
                'adaptability': adaptability, 'culture': culture, 'digital': digital,
                'school_support': school_support, 'peer': peer
            }.items())
    )

    min_score = (
        prob * 100 * weights['prob'] +
        sum(0.3 * 100 * weights[key] for key in weights if key != 'prob')
    )
    max_score = (
        prob * 100 * weights['prob'] +
        sum(0.9 * 100 * weights[key] for key in weights if key != 'prob')
    )

    return round(min_score, 2), round(expected, 2), round(max_score, 2)

app.layout = html.Div([
    html.H2("Study Abroad Decision Network"),

    html.Label("Academic Performance"),
    dcc.RadioItems(['High', 'Average', 'Low'], 'High', id='academic'),

    html.Label("Language Proficiency"),
    dcc.RadioItems(['Excellent', 'Moderate', 'Poor'], 'Excellent', id='language'),

    html.Label("Target Country"),
    dcc.RadioItems(['Germany', 'UK', 'Netherlands', 'USA'], 'Germany', id='country'),

    html.Label("Field of Study"),
    dcc.RadioItems(['STEM', 'Arts', 'Business', 'Social Sciences', 'Health'], 'STEM', id='field'),

    html.Label("Financial Resources"),
    dcc.RadioItems(['Stable', 'Volatile', 'In Debt'], 'Stable', id='finance'),

    html.Label("Support Network"),
    dcc.RadioItems(['Strong', 'Average', 'None'], 'Strong', id='support'),

    html.Label("Arts Engagement"),
    dcc.RadioItems(['High', 'Moderate', 'Low'], 'Moderate', id='arts'),

    html.Label("Portfolio Strength"),
    dcc.RadioItems(['Strong', 'Average', 'Weak'], 'Average', id='portfolio'),

    html.Label("Visa Policy Friendliness"),
    dcc.RadioItems(['Supportive', 'Neutral', 'Restrictive'], 'Supportive', id='visa'),

    html.Label("Tuition Cost Level"),
    dcc.RadioItems(['Low', 'Moderate', 'High'], 'Moderate', id='tuition'),

    html.Label("Post-Study Work Rights"),
    dcc.RadioItems(['Generous', 'Limited', 'None'], 'Generous', id='work_rights'),

    html.Label("Adaptability / Resilience"),
    dcc.RadioItems(['High', 'Medium', 'Low'], 'High', id='adaptability'),

    html.Label("Cultural Openness"),
    dcc.RadioItems(['Open', 'Neutral', 'Reserved'], 'Open', id='culture'),

    html.Label("Digital Literacy"),
    dcc.RadioItems(['Advanced', 'Basic', 'Limited'], 'Advanced', id='digital'),

    html.Label("School Support Quality"),
    dcc.RadioItems(['Strong', 'Average', 'Weak'], 'Strong', id='school_support'),

    html.Label("Peer Influence"),
    dcc.RadioItems(['Encouraging', 'Neutral', 'Discouraging'], 'Encouraging', id='peer'),

    html.Br(),
    html.Div(id='output')
], style={'padding': '16px', 'fontFamily': 'Arial', 'fontSize': '10px'})

@app.callback(
    Output('output', 'children'),
    Input('academic', 'value'),
    Input('language', 'value'),
    Input('country', 'value'),
    Input('field', 'value'),
    Input('finance', 'value'),
    Input('support', 'value'),
    Input('arts', 'value'),
    Input('portfolio', 'value'),
    Input('visa', 'value'),
    Input('tuition', 'value'),
    Input('work_rights', 'value'),
    Input('adaptability', 'value'),
    Input('culture', 'value'),
    Input('digital', 'value'),
    Input('school_support', 'value'),
    Input('peer', 'value')
)
def update_output(academic, language, country, field, finance, support, arts, portfolio,
                  visa, tuition, work_rights, adaptability, culture, digital, school_support, peer):
    prob = get_study_abroad_prob(academic, language, country, field)
    min_score, expected_score, max_score = compute_utility_range(
        prob, finance, support, arts, portfolio, visa, tuition, work_rights,
        adaptability, culture, digital, school_support, peer
    )
    return html.Div([
        html.P(f"Estimated Probability of Studying Abroad: {prob:.2f}"),
        html.P(f"Expected Readiness Score: {expected_score}/100"),
        html.P(f"Score Range: {min_score} – {max_score}/100")
    ])

if __name__ == '__main__':
    app.run(debug=False)
