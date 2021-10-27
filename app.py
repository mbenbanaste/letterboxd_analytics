import os
from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.io as pio
from functions import number_of_unique_values_in_column, most_watched_column_per_release_year, \
    how_many_films_per_decade, average_per_decade_df, most_watched_column_per_decade, \
    highest_rated_column_per_decade, how_many_column, average_rated_column, \
    most_watched_actors_or_directors_per_genre, most_watched_actors_or_directors_per_country, \
    average_ratings_of_actor_or_director_per_genre, average_ratings_of_actor_or_director_per_country, \
    most_watched_actors_or_directors, average_rating_of_actor_or_director, \
    highest_rated_column_between_years, most_watched_column_between_years

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
# file = pd.read_csv(os.path.join(directory_of_python_script, "data.csv"))
file = r'/Users/mbenbanaste/Documents/GitHub/letterboxd_analytics/data.csv'
dff = pd.read_csv(file)
df = pd.DataFrame(dff)


@app.route('/')
def index():
    number_of_films = len(df)
    number_of_minutes = sum(df['Minutes'])
    number_of_hours = number_of_minutes / 60
    number_of_directors = number_of_unique_values_in_column('Director')
    number_of_countries = number_of_unique_values_in_column('Countries')

    return render_template('index.html',
                           number_of_films=number_of_films,
                           number_of_minutes=number_of_minutes,
                           number_of_hours=number_of_hours,
                           number_of_directors=number_of_directors,
                           number_of_countries=number_of_countries)


@app.route('/how_many_films_per_year')
def app_how_many_films_per_year():
    films_per_year_df = df[['Films', 'Year']]

    fig = px.histogram(films_per_year_df, x="Year",
                     template='plotly_dark')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash2.html',
                           graphJSON=graphJSON
                           )


@app.route('/average_rating_per_year')
def app_average_rating_per_year():
    films_per_year_average_rating_df = df[['My Ratings', 'Year']]
    films_per_year_average_rating_df = films_per_year_average_rating_df.groupby(['Year']).mean()
    films_per_year_average_rating_df = films_per_year_average_rating_df.reset_index()

    fig = px.bar(x=films_per_year_average_rating_df['Year'], y=films_per_year_average_rating_df['My Ratings'],
                     template='plotly_dark')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash2.html',
                           graphJSON=graphJSON
                           )


@app.route('/how_many_per_genre')
def app_how_many_per_genre():
    fig = how_many_column('Genres')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash2.html',
                           graphJSON=graphJSON
                           )


@app.route('/how_many_per_country')
def app_how_many_per_country():
    fig = how_many_column('Countries')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash2.html',
                           graphJSON=graphJSON
                           )


@app.route('/average_rated_column_', methods=['POST', 'GET'])
def app_average_rated_column():
    tvalues = ['Genres', 'Countries']

    min_ = []
    for x in range(1, 101):
        min_.append(x)

    return render_template('2_input_genrecountry_threshold_avg.html',
                           option_list1=tvalues,
                           option_list2=min_
                           )

def create_graph_average_rated_column(x='Countries', y=1):

    fig = average_rated_column(x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_average_rated_column', methods=['POST', 'GET'])
def change_features_average_rated_column():
    return create_graph_average_rated_column(request.args.get('x'), int(request.args.get('y')))


@app.route('/most_watched_column_per_release_year_', methods=['POST', 'GET'])
def app_most_watched_column_per_release_year():
    tvalues = ['Genres', 'Countries']
    yvalues = list(df['Year'].unique())

    return render_template('2_input_genrecountry_year.html',
                           option_list1=tvalues,
                           option_list2=yvalues
                           )

def create_graph_most_watched_column_per_release_year(x='Countries', y=1990):

    fig = most_watched_column_per_release_year(x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_most_watched_column_per_release_year', methods=['POST', 'GET'])
def change_features_most_watched_column_per_release_year():
    return create_graph_most_watched_column_per_release_year(request.args.get('x'), int(request.args.get('y')))



@app.route('/how_many_films_per_decade_', methods=['POST', 'GET'])
def app_how_many_films_per_decade():
    fig = how_many_films_per_decade()

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("notdash2.html",
                           graphJSON=graphJSON
                           )


@app.route('/average_per_decade_', methods=['POST', 'GET'])
def app_average_per_decade():
    fig = average_per_decade_df()

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("notdash2.html",
                           graphJSON=graphJSON
                           )


@app.route('/most_watched_column_per_decade_', methods=['POST', 'GET'])
def app_most_watched_column_per_decade():
    tvalues = ['Genres', 'Countries', 'Director', 'Actors']

    most_watched_per_decade_dff = df[['Year']]
    most_watched_per_decade_dff['Decade'] = most_watched_per_decade_dff['Year'].copy()
    for i in range(0, len(most_watched_per_decade_dff)):
        most_watched_per_decade_dff['Decade'][i] = str(most_watched_per_decade_dff['Year'][i])[:3] + '0s'
    decades = list(most_watched_per_decade_dff['Decade'].unique())

    top_ = ['All']
    for x in range(1, 26):
        top_.append(x)

    return render_template('3_input_4column_perdecade_min_count.html', option_list1=tvalues, option_list2=decades, option_list3=top_)

def create_graph_most_watched_column_per_decade(x='Director', y='1990s', z=3):

    if z != 'All':
        z = int(z)

    fig = most_watched_column_per_decade(x, y, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_most_watched_column_per_decade', methods=['POST', 'GET'])
def change_features_most_watched_column_per_decade():
    return create_graph_most_watched_column_per_decade(request.args.get('x'), request.args.get('y'), int(request.args.get('z')))


@app.route('/highest_rated_column_per_decade_', methods=['POST', 'GET'])
def app_highest_rated_column_per_decade():
    tvalues = ['Genres', 'Countries', 'Director', 'Actors']

    highest_rated_per_decade_df = df[['Year']]
    highest_rated_per_decade_df['Decade'] = highest_rated_per_decade_df['Year'].copy()
    for i in range(0, len(highest_rated_per_decade_df)):
        highest_rated_per_decade_df['Decade'][i] = str(highest_rated_per_decade_df['Year'][i])[:3] + '0s'
    decades = list(highest_rated_per_decade_df['Decade'].unique())

    min_ = []
    for x in range(0, 11):
        min_.append(x)

    return render_template('3_input_4column_perdecade_min_avg.html', option_list1=tvalues, option_list2=decades, option_list3=min_)

def create_graph_highest_rated_column_per_decade(x='Director', y='1990s', z=3):
    fig = highest_rated_column_per_decade(x, y, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_highest_rated_column_per_decade', methods=['POST', 'GET'])
def change_features_highest_rated_column_per_decade():
    return create_graph_highest_rated_column_per_decade(request.args.get('x'), request.args.get('y'), int(request.args.get('z')))


@app.route('/most_watched_actors_or_directors_per_genre_', methods=['POST', 'GET'])
def app_most_watched_actors_or_directors_per_genre():
    tvalues = ['Director', 'Actors']

    x = df['Genres']
    l = []
    for i in range(0, len(x)):
        if type(x[i]) == str:
            y = x[i].split(', ')
            l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    genres = sorted(list(set(ll)))

    min_ = []
    for x in range(0, 11):
        min_.append(x)

    return render_template('3_input_directororactor_genre_min_count.html',
                           option_list1=tvalues, option_list2=genres, option_list3=min_)

def create_graph_most_watched_actors_or_directors_per_genre(x='Director', y='Action', z=3):
    fig = most_watched_actors_or_directors_per_genre(x, y, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_most_watched_actors_or_directors_per_genre', methods=['POST', 'GET'])
def change_features_most_watched_actors_or_directors_per_genre():
    return create_graph_most_watched_actors_or_directors_per_genre(request.args.get('x'), request.args.get('y'), int(request.args.get('z')))


@app.route('/most_watched_actors_or_directors_per_country_', methods=['POST', 'GET'])
def app_most_watched_actors_or_directors_per_country():
    tvalues = ['Director', 'Actors']

    x = df['Countries']
    l = []
    for i in range(0, len(x)):
        if type(x[i]) == str:
            y = x[i].split(', ')
            l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    countries = sorted(list(set(ll)))

    min_ = []
    for x in range(0, 11):
        min_.append(x)

    return render_template('3_input_directororactor_country_min_avg.html',
                           option_list1=tvalues, option_list2=countries, option_list3=min_)

def create_graph_most_watched_actors_or_directors_per_country(x='Director', y='France', z=3):
    fig = most_watched_actors_or_directors_per_country(x, y, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_most_watched_actors_or_directors_per_country', methods=['POST', 'GET'])
def change_features_most_watched_actors_or_directors_per_country():
    return create_graph_most_watched_actors_or_directors_per_country(request.args.get('x'), request.args.get('y'), int(request.args.get('z')))


@app.route('/average_ratings_of_actor_or_director_per_genre_', methods=['POST', 'GET'])
def app_average_ratings_of_actor_or_director_per_genre():
    tvalues = ['Director', 'Actors']

    x = df['Genres']
    l = []
    for i in range(0, len(x)):
        if type(x[i]) == str:
            y = x[i].split(', ')
            l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    genres = sorted(list(set(ll)))

    min_ = []
    for x in range(0, 11):
        min_.append(x)

    return render_template('3_input_directororactor_genre_min_avg.html',
                           option_list1=tvalues, option_list2=genres, option_list3=min_)

def create_graph_average_ratings_of_actor_or_director_per_genre(x='Director', y='Action', z=3):
    fig = average_ratings_of_actor_or_director_per_genre(x, y, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_average_ratings_of_actor_or_director_per_genre', methods=['POST', 'GET'])
def change_features_average_ratings_of_actor_or_director_per_genre():
    return create_graph_average_ratings_of_actor_or_director_per_genre(request.args.get('x'), request.args.get('y'), int(request.args.get('z')))


@app.route('/average_ratings_of_actor_or_director_per_country_', methods=['POST', 'GET'])
def app_average_ratings_of_actor_or_director_per_country():
    tvalues = ['Director', 'Actors']

    x = df['Countries']
    l = []
    for i in range(0, len(x)):
        if type(x[i]) == str:
            y = x[i].split(', ')
            l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    countries = sorted(list(set(ll)))

    min_ = []
    for x in range(0, 11):
        min_.append(x)

    return render_template('3_input_directororactor_country_min_avg.html',
                           option_list1=tvalues, option_list2=countries, option_list3=min_)

def create_graph_average_ratings_of_actor_or_director_per_country(x='Director', y='France', z=3):
    fig = average_ratings_of_actor_or_director_per_country(x, y, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_average_ratings_of_actor_or_director_per_country', methods=['POST', 'GET'])
def change_features_average_ratings_of_actor_or_director_per_country():
    return create_graph_average_ratings_of_actor_or_director_per_country(request.args.get('x'), request.args.get('y'), int(request.args.get('z')))


@app.route('/most_watched_actors_or_directors_', methods=['POST', 'GET'])
def app_most_watched_actors_or_directors():
    tvalues = ['Director', 'Actors']

    top_ = ['All']
    for x in range(1, 100):
        top_.append(x)

    return render_template("2_input_directororactor_threshold_avg.html",
                           option_list1=tvalues,
                           option_list2=top_,
                           graphJSON=create_graph_most_watched_actors_or_directors()
                           )

def create_graph_most_watched_actors_or_directors(x='Director', y=2):
    fig = most_watched_actors_or_directors(x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_most_watched_actors_or_directors', methods=['POST', 'GET'])
def change_features_most_watched_actors_or_directors():
    return create_graph_most_watched_actors_or_directors(request.args.get('x'), int(request.args.get('y')))


@app.route('/average_rating_of_actor_or_director', methods=['POST', 'GET'])
def app_average_rating_of_actor_or_director():
    tvalues = ['Director', 'Actors']

    min_ = []
    for x in range(0, 21):
        min_.append(x)

    return render_template('2_input_directororactor_threshold_avg.html',
                           option_list1=tvalues,
                           option_list2=min_,
                           graphJSON=create_graph_average_rating_of_actor_or_director()
                           )


def create_graph_average_rating_of_actor_or_director(x='Director', y=5):
    fig = average_rating_of_actor_or_director(x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_average_rating_of_actor_or_director', methods=['POST', 'GET'])
def change_features_average_rating_of_actor_or_director():
    return create_graph_average_rating_of_actor_or_director(request.args.get('x'), int(request.args.get('y')))


@app.route('/highest_rated_column_between_years', methods=['POST', 'GET'])
def app_highest_rated_column_between_years():
    tvalues = ['Director', 'Actors', 'Countries', 'Genres']

    now = datetime.now()
    this_year = now.year
    this_year

    year = []
    for x in range(1915, this_year+1):
        year.append(x)

    year_ = []
    for x in range(1915, this_year+1):
        year_.append(x)

    min_ = []
    for x in range(0, 21):
        min_.append(x)

    # header = ""
    # description = """
    # """

    return render_template('4_input_directororactororgenreorcountries_between_years.html',
                           option_list1=tvalues,
                           option_list2=year,
                           option_list3=year_,
                           option_list4=min_,
                           graphJSON=create_graph_highest_rated_column_between_years(),
                           # header=header,
                           # description=description
                           )


def create_graph_highest_rated_column_between_years(x='Director', y=1960, y_=1980, z=2):
    fig = highest_rated_column_between_years(x, y, y_, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_highest_rated_column_between_years', methods=['POST', 'GET'])
def change_features_highest_rated_column_between_years():
    return create_graph_highest_rated_column_between_years(request.args.get('x'), int(request.args.get('y')), int(request.args.get('y_')), int(request.args.get('z')))


@app.route('/most_watched_column_between_years', methods=['POST', 'GET'])
def app_most_watched_column_between_years():
    tvalues = ['Director', 'Actors', 'Countries', 'Genres']

    now = datetime.now()
    this_year = now.year
    this_year

    year = []
    for x in range(1915, this_year+1):
        year.append(x)

    year_ = []
    for x in range(1915, this_year+1):
        year_.append(x)

    min_ = []
    for x in range(0, 21):
        min_.append(x)

    return render_template('4_input_directororactororgenreorcountries_between_years_count.html',
                           option_list1=tvalues,
                           option_list2=year,
                           option_list3=year_,
                           option_list4=min_,
                           graphJSON=create_graph_most_watched_column_between_years()
                           )


def create_graph_most_watched_column_between_years(x='Director', y=1960, y_=1980, z=2):
    fig = most_watched_column_between_years(x, y, y_, z)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/change_features_most_watched_column_between_years', methods=['POST', 'GET'])
def change_features_most_watched_column_between_years():
    return create_graph_most_watched_column_between_years(request.args.get('x'), int(request.args.get('y')), int(request.args.get('y_')), int(request.args.get('z')))
