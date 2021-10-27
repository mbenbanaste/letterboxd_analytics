import os
import plotly.express as px
import plotly.io as pio
import pandas as pd

# directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
# file = pd.read_csv(os.path.join(directory_of_python_script, "data.csv"))
file = r'/Users/mbenbanaste/Documents/GitHub/letterboxd_analytics/data.csv'
dff = pd.read_csv(file)
df = pd.DataFrame(dff)


def number_of_unique_values_in_column(column):
    colum_values = df[df[f'{column}'].notnull()]
    colum_values = colum_values[f'{column}']
    l = []
    for k in range(0, len(colum_values)):
        colum_values_ = list(colum_values)[k].split(', ')
        no_of_colum_values = len(colum_values_)
        if no_of_colum_values == 1:
            l.append(colum_values_[0])
        if no_of_colum_values > 1:
            for x in colum_values_:
                l.append(x)
    return len(set(l))


def most_watched_column_per_release_year(column, year):
    most_watched_per_release_year = df[[f'{column}', 'Year']]

    x = most_watched_per_release_year[most_watched_per_release_year['Year'] == year]
    x = list(x[f'{column}'])

    l = []
    for i in range(0, len(x)):
        y = x[i].split(', ')
        l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    lll = pd.DataFrame(list(ll))
    lll.value_counts()
    lll = lll.value_counts().rename_axis(f'{column}').reset_index(name='counts')

    if column == 'Genres':
        fig = px.bar(lll, x=f'{column}', y='counts',
                     title=f'How many films per genre in {year}',
                     template='plotly_dark')

    else:
        fig = px.bar(lll, x=f'{column}', y='counts',
                     title=f'How many films per country in {year}',
                     template='plotly_dark')

    return fig


def how_many_films_per_decade():
    films_per_decade_df = df[['Films', 'Year']]
    films_per_decade_df = films_per_decade_df.groupby(['Year']).count()
    films_per_decade_df = films_per_decade_df.reset_index()

    films_per_decade_df['Decade'] = films_per_decade_df['Year'].copy()
    for i in range(0, len(films_per_decade_df)):
        films_per_decade_df['Decade'][i] = str(films_per_decade_df['Year'][i])[:3] + '0s'

    films_per_decade_df.groupby(['Decade']).sum()
    films_per_decade_df = films_per_decade_df.reset_index(drop=True)

    fig = px.bar(films_per_decade_df, x='Decade', y='Films', color='Year',
                 title=f'How many films per decade',
                     template='plotly_dark')

    return fig


def average_per_decade_df():
    average_per_decade_df = df[['My Ratings', 'Year']]
    average_per_decade_df = average_per_decade_df.groupby(['Year']).mean()
    average_per_decade_df = average_per_decade_df.reset_index()

    average_per_decade_df['Decade'] = average_per_decade_df['Year'].copy()
    for i in range(0, len(average_per_decade_df)):
        average_per_decade_df['Decade'][i] = str(average_per_decade_df['Year'][i])[:3] + '0s'

    average_per_decade_df.drop(columns=['Year'], inplace=True)
    average_per_decade_df = average_per_decade_df.groupby(['Decade']).mean()
    average_per_decade_df = average_per_decade_df.reset_index()

    fig = px.bar(average_per_decade_df, x='Decade', y='My Ratings',
                 title=f'My average ratings per decade',
                     template='plotly_dark')

    return fig


def most_watched_column_per_decade(column, decade, top_=None):
    most_watched_per_decade_df = df[[f'{column}', 'Year']]

    most_watched_per_decade_df['Decade'] = most_watched_per_decade_df['Year'].copy()
    for i in range(0, len(most_watched_per_decade_df)):
        most_watched_per_decade_df['Decade'][i] = str(most_watched_per_decade_df['Year'][i])[:3] + '0s'

    x = most_watched_per_decade_df[most_watched_per_decade_df['Decade'] == decade]
    x = list(x[f'{column}'])

    l = []
    for i in range(0, len(x)):
        if type(x[i]) == str:
            y = x[i].split(', ')
            l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    lll = pd.DataFrame(list(ll))
    lll.value_counts()
    lll = lll.value_counts().rename_axis(f'{column}').reset_index(name='counts')
    if top_ == 'All':
        top_ = len(lll)
    else:
        top_ = top_

    lll = lll.head(top_)

    if top_ == None:
        if column == 'Director':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {column} in {decade}',
                     template='plotly_dark')

        if column == 'Actors':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {column} in {decade}',
                     template='plotly_dark')

        if column == 'Countries':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {column} in {decade}',
                     template='plotly_dark')

        if column == 'Genres':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {column} in {decade}',
                     template='plotly_dark')

    else:
        if column == 'Director':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {top_} {column} in {decade}',
                     template='plotly_dark')

        if column == 'Actors':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {top_} {column} in {decade}',
                     template='plotly_dark')

        if column == 'Countries':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {top_} {column} in {decade}',
                     template='plotly_dark')

        if column == 'Genres':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {top_} {column} in {decade}',
                     template='plotly_dark')

    return fig


def highest_rated_column_per_decade(column, decade, min_=0):
    highest_rated_per_decade_df = df[[f'{column}', 'My Ratings', 'Year']]

    highest_rated_per_decade_df['Decade'] = highest_rated_per_decade_df['Year'].copy()
    for i in range(0, len(highest_rated_per_decade_df)):
        highest_rated_per_decade_df['Decade'][i] = str(highest_rated_per_decade_df['Year'][i])[:3] + '0s'
    highest_rated_per_decade_df = highest_rated_per_decade_df.dropna()

    highest_rated_per_decade_df.drop(columns=['Year'], inplace=True)
    highest_rated_per_decade_df = highest_rated_per_decade_df[highest_rated_per_decade_df['Decade'] == decade]
    highest_rated_per_decade_df.drop(columns=['Decade'], inplace=True)

    x = highest_rated_per_decade_df

    l = []
    for i in range(0, len(x)):
        y = x['My Ratings'].tolist()
        xx = x[f'{column}'].tolist()
        xx = xx[i].split(', ')
        for j in range(0, len(xx)):
            l.append([y[i], xx[j]])

    ratings = []
    genre = []
    for i in range(0, len(l)):
        ratings.append(l[i][0])
        genre.append(l[i][1])

    data = {f'{column}': genre, 'My Ratings': ratings}
    xx = pd.DataFrame(data)
    vc = xx[f'{column}'].value_counts()
    xx = xx[xx[f'{column}'].isin(vc.index[vc.gt(min_)])]
    xx = xx.groupby([f'{column}']).mean()
    xx = xx.sort_values(['My Ratings'], ascending=[0])
    xx = xx.reset_index()

    if column == 'Director':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column}s whose I have seen at least {min_} films in {decade}',
                     template='plotly_dark')

    if column == 'Actors':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column} whose I have seen at least {min_} films in {decade}',
                     template='plotly_dark')

    if column == 'Countries':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of films from {column} from which I have seen at least {min_} films in {decade}',
                     template='plotly_dark')

    if column == 'Genres':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column} from which I have seen at least {min_} films in {decade}',
                     template='plotly_dark')

    return fig


def how_many_column(column, top_=None):
    films_per_column = df[f'{column}'].dropna()
    films_per_column = films_per_column.tolist()
    l = []
    for i in range(0, len(films_per_column)):
        film_ = films_per_column[i].split(', ')
        l.append(film_)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    lll = pd.DataFrame(list(ll))
    lll.value_counts()
    lll = lll.value_counts().rename_axis(f'{column}').reset_index(name='counts')
    lll = lll.head(top_)
    lll = lll.sort_values(by='counts', ascending=True)

    fig = px.bar(lll, y=f'{column}', x='counts', orientation='h',
                 title=f'How many films per {column}',
                 labels=dict(y=f'{column}', x="Counts"),
                     template='plotly_dark')

    return fig


def average_rated_column(column, min_=1):
    average_rated_column = df[['My Ratings', f'{column}']]
    average_rated_column = average_rated_column.dropna()

    l = []
    for i in range(0, len(average_rated_column)):
        y = average_rated_column['My Ratings'].tolist()
        x = average_rated_column[f'{column}'].tolist()
        x = x[i].split(', ')
        for j in range(0, len(x)):
            l.append([y[i], x[j]])

    ratings = []
    genre = []
    for i in range(0, len(l)):
        ratings.append(l[i][0])
        genre.append(l[i][1])

    data = {'My Ratings': ratings, f'{column}': genre}
    xx = pd.DataFrame(data)
    vc = xx[f'{column}'].value_counts()
    xx = xx[xx[f'{column}'].isin(vc.index[vc.gt(min_)])]
    xx = xx.groupby([f'{column}']).mean()
    xx = xx.sort_values(['My Ratings'], ascending=[0])
    xx = xx.reset_index()

    if column == 'Genres':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                #  orientation='h',
                title=f'My average rating of {column} that I have seen at least {min_} films of',
                     template='plotly_dark')

    else:
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                #  orientation='h',
                title=f'My average rating of films from {column} from which I have seen at least {min_} films',
                     template='plotly_dark')

    return fig


def most_watched_actors_or_directors_per_genre(column, genre, min_=1):
    most_watched_actors_or_directors_per_genre = df[[f'{column}', 'Genres']]
    most_watched_actors_or_directors_per_genre = most_watched_actors_or_directors_per_genre.dropna()

    l = []
    for i in range(0, len(most_watched_actors_or_directors_per_genre)):
        y = most_watched_actors_or_directors_per_genre[f'{column}'].tolist()
        y = y[i].split(', ')
        x = most_watched_actors_or_directors_per_genre['Genres'].tolist()
        x = x[i].split(', ')
        for j in range(0, len(x)):
            for jj in range(0, len(y)):
                l.append([y[jj], x[j]])

    directors = []
    genre_ = []
    for i in range(0, len(l)):
        directors.append(l[i][0])
        genre_.append(l[i][1])

    data = {f'{column}': directors, 'Genres': genre_}
    xx = pd.DataFrame(data)
    xx = xx[xx['Genres'] == f'{genre}']
    xx = xx.groupby([f'{column}']).count()
    xx = xx.sort_values(['Genres'], ascending=[0])
    xx = xx.reset_index()
    xx.rename(columns={'Genres': 'Counts'}, inplace=True)
    xx = xx[xx['Counts'] > min_]

    if column == 'Director':
        xx.rename(columns={f'{column}': f'{column}s in {genre} films'}, inplace=True)
        fig = px.bar(xx, x=f'{column}s in {genre} films', y='Counts',
                     #  orientation='h',
                     title=f'Most watched {column}s whose I have seen at least {min_} {genre} films',
                     template='plotly_dark')

    else:
        xx.rename(columns={f'{column}': f'{column} in {genre} films'}, inplace=True)
        fig = px.bar(xx, x=f'{column} in {genre} films', y='Counts',
                     #  orientation='h',
                     title=f'Most watched {column} whose I have seen at least {min_} {genre} films',
                     template='plotly_dark')

    return fig


def most_watched_actors_or_directors_per_country(column, country, min_=1):
    most_watched_actors_or_directors_per_country = df[[f'{column}', 'Countries']]
    most_watched_actors_or_directors_per_country = most_watched_actors_or_directors_per_country.dropna()

    l = []
    for i in range(0, len(most_watched_actors_or_directors_per_country)):
        y = most_watched_actors_or_directors_per_country[f'{column}'].tolist()
        y = y[i].split(', ')
        x = most_watched_actors_or_directors_per_country['Countries'].tolist()
        x = x[i].split(', ')
        for j in range(0, len(x)):
            for jj in range(0, len(y)):
                l.append([y[jj], x[j]])

    directors = []
    countries_ = []
    for i in range(0, len(l)):
        directors.append(l[i][0])
        countries_.append(l[i][1])

    data = {f'{column}': directors, 'Countries': countries_}
    xx = pd.DataFrame(data)
    xx = xx[xx['Countries'] == f'{country}']
    xx = xx.groupby([f'{column}']).count()
    xx = xx.sort_values(['Countries'], ascending=[0])
    xx = xx.reset_index()
    xx.rename(columns={'Countries': 'Counts'}, inplace=True)
    xx = xx[xx['Counts'] > min_]

    if column == 'Director':
        xx.rename(columns={f'{column}': f'{column}s from {country}'}, inplace=True)
        fig = px.bar(xx, x=f'{column}s from {country}', y='Counts',
                     #  orientation='h',
                     title=f'Most watched {column}s from {country} whose I have seen at least {min_} films',
                     template='plotly_dark')

    else:
        xx.rename(columns={f'{column}': f'{column} from {country}'}, inplace=True)
        fig = px.bar(xx, x=f'{column} from {country}', y='Counts',
                     #  orientation='h',
                     title=f'Most watched {column} from {country} whose I have seen at least {min_} films',
                     template='plotly_dark')

    return fig


def average_ratings_of_actor_or_director_per_genre(column, genre, min_=1):
    average_ratings_of_actor_or_director_per_genre = df[[f'{column}', 'My Ratings', 'Genres']]
    average_ratings_of_actor_or_director_per_genre = average_ratings_of_actor_or_director_per_genre.dropna()

    l = []
    for i in range(0, len(average_ratings_of_actor_or_director_per_genre)):
        y = average_ratings_of_actor_or_director_per_genre['My Ratings'].tolist()
        x = average_ratings_of_actor_or_director_per_genre[f'{column}'].tolist()
        x = x[i].split(', ')
        z = average_ratings_of_actor_or_director_per_genre['Genres'].tolist()
        z = z[i].split(', ')
        for j in range(0, len(x)):
            for jj in range(0, len(z)):
                l.append([y[i], x[j], z[jj]])

    ratings = []
    actors = []
    genre_ = []
    for i in range(0, len(l)):
        ratings.append(l[i][0])
        actors.append(l[i][1])
        genre_.append(l[i][2])

    data = {'My Ratings': ratings, f'{column}': actors, f'{genre}': genre_}
    xx = pd.DataFrame(data)
    xx = xx[xx[f'{genre}'] == f'{genre}']
    vc = xx[f'{column}'].value_counts()
    xx = xx[xx[f'{column}'].isin(vc.index[vc.gt(min_)])]
    xx = xx.groupby([f'{column}']).mean()
    xx = xx.sort_values(['My Ratings'], ascending=[0])
    xx = xx.reset_index()

    if column == 'Director':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column}s whose I have seen at least {min_} {genre} films',
                     template='plotly_dark')

    else:
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column} whose I have seen at least {min_} {genre} films',
                     template='plotly_dark')

    return fig


def average_ratings_of_actor_or_director_per_country(column, country, min_=1):
    average_ratings_of_actor_or_director_per_country = df[[f'{column}', 'My Ratings', 'Countries']]
    average_ratings_of_actor_or_director_per_country = average_ratings_of_actor_or_director_per_country.dropna()

    l = []
    for i in range(0, len(average_ratings_of_actor_or_director_per_country)):
        y = average_ratings_of_actor_or_director_per_country['My Ratings'].tolist()
        x = average_ratings_of_actor_or_director_per_country[f'{column}'].tolist()
        x = x[i].split(', ')
        z = average_ratings_of_actor_or_director_per_country['Countries'].tolist()
        z = z[i].split(', ')
        for j in range(0, len(x)):
            for jj in range(0, len(z)):
                l.append([y[i], x[j], z[jj]])

    ratings = []
    actors = []
    country_ = []
    for i in range(0, len(l)):
        ratings.append(l[i][0])
        actors.append(l[i][1])
        country_.append(l[i][2])

    data = {'My Ratings': ratings, f'{column}': actors, f'{country}': country_}
    xx = pd.DataFrame(data)
    xx = xx[xx[f'{country}'] == f'{country}']
    vc = xx[f'{column}'].value_counts()
    xx = xx[xx[f'{column}'].isin(vc.index[vc.gt(min_)])]
    xx = xx.groupby([f'{column}']).mean()
    xx = xx.sort_values(['My Ratings'], ascending=[0])
    xx = xx.reset_index()

    if column == 'Director':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column}s from {country} whose I have seen at least {min_} films',
                     template='plotly_dark')

    else:
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column} from {country} whose I have seen at least {min_} films',
                     template='plotly_dark')

    return fig


def most_watched_actors_or_directors(column, top_=None):
    most_watched_actors_or_directors = df[[f'{column}']]
    most_watched_actors_or_directors = most_watched_actors_or_directors.dropna()

    l = []
    for i in range(0, len(most_watched_actors_or_directors)):
        y = most_watched_actors_or_directors[f'{column}'].tolist()
        y = y[i].split(', ')
        for j in range(0, len(y)):
            l.append(y[j])

    lll = pd.DataFrame(list(l))
    lll.value_counts()
    lll = lll.value_counts().rename_axis(f'{column}').reset_index(name='counts')

    if top_ == 'All':
        top_ = len(l)
    else:
        top_ = top_

    lll = lll.head(top_)

    if top_ == None:
        if column == 'Director':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {column}s',
                     template='plotly_dark')

        else:
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {column}',
                     template='plotly_dark')
    else:
        if column == 'Director':
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {top_} {column}s',
                     template='plotly_dark')

        else:
            fig = px.bar(lll, x=f'{column}', y='counts',
                         #  orientation='h',
                         title=f'Most watched {top_} {column}',
                     template='plotly_dark')

    return fig

def average_rating_of_actor_or_director(column, min_=2):
    average_ratings_of_actor_or_director_per_genre = df[[f'{column}','My Ratings']]
    average_ratings_of_actor_or_director_per_genre = average_ratings_of_actor_or_director_per_genre.dropna()

    l = []
    for i in range(0, len(average_ratings_of_actor_or_director_per_genre)):
        y = average_ratings_of_actor_or_director_per_genre['My Ratings'].tolist()
        x = average_ratings_of_actor_or_director_per_genre[f'{column}'].tolist()
        x = x[i].split(', ')
        for j in range(0, len(x)):
            l.append([y[i], x[j]])

    ratings = []
    actors_ = []
    for i in range(0, len(l)):
        ratings.append(l[i][0])
        actors_.append(l[i][1])

    data = {'My Ratings': ratings, f'{column}': actors_}
    xx = pd.DataFrame(data)
    vc = xx[f'{column}'].value_counts()
    xx = xx[xx[f'{column}'].isin(vc.index[vc.gt(min_)])]
    xx = xx.groupby([f'{column}']).mean()
    xx = xx.sort_values(['My Ratings'], ascending=[0])
    xx = xx.reset_index()

    if column == 'Director':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  orientation='h',
                     title=f'My average rating of {column}s whose I have seen at least {min_} films',
                     template='plotly_dark')

    else:
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  orientation='h',
                     title=f'My average rating of {column} whose I have seen at least {min_} films',
                     template='plotly_dark')

    return fig


def highest_rated_column_between_years(column, year, year_, min_=1):
    highest_rated_per_decade_df = df[[f'{column}', 'My Ratings', 'Year']]

    xf = highest_rated_per_decade_df.dropna()
    xf = xf[xf['Year'] >= year]
    xf = xf[xf['Year'] <= year_]
    xf.drop(columns=['Year'], inplace=True)

    l = []
    for i in range(0, len(xf)):
        y = xf['My Ratings'].tolist()
        xx = xf[f'{column}'].tolist()
        xx = xx[i].split(', ')
        for j in range(0, len(xx)):
            l.append([y[i], xx[j]])

    ratings = []
    genre = []
    for i in range(0, len(l)):
        ratings.append(l[i][0])
        genre.append(l[i][1])

    data = {f'{column}': genre, 'My Ratings': ratings}
    xx = pd.DataFrame(data)
    vc = xx[f'{column}'].value_counts()
    xx = xx[xx[f'{column}'].isin(vc.index[vc.gt(min_)])]
    xx = xx.groupby([f'{column}']).mean()
    xx = xx.sort_values(['My Ratings'], ascending=[0])
    xx = xx.reset_index()

    if column == 'Director':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column}s whose I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    if column == 'Actors':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column} whose I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    if column == 'Countries':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of films from {column} from which I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    if column == 'Genres':
        fig = px.bar(xx, x=f'{column}', y='My Ratings',
                     #  color=f'{column}',
                     #  orientation='h',
                     title=f'My average rating of {column} from which I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    return fig


def most_watched_column_between_years(column, year, year_, min_=1):
    xf = df[[f'{column}', 'Year']]

    xf = xf[xf['Year'] >= year]
    xf = xf[xf['Year'] <= year_]
    xf.drop(columns=['Year'], inplace=True)
    x = list(xf[f'{column}'])

    l = []
    for i in range(0, len(x)):
        y = x[i].split(', ')
        l.append(y)

    ll = []
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            ll.append(l[i][j])

    lll = pd.DataFrame(list(ll))
    lll.value_counts()
    lll = lll.value_counts().rename_axis(f'{column}').reset_index(name='counts')
    lll = lll[lll['counts'] > min_]

    if column == 'Director':
        fig = px.bar(lll, x=f'{column}', y='counts',
                     title=f'How many films of directors whose I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    if column == 'Actors':
        fig = px.bar(lll, x=f'{column}', y='counts',
                     title=f'How many films of actors whose I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    if column == 'Countries':
        fig = px.bar(lll, x=f'{column}', y='counts',
                     title=f'How many films per country from which I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    if column == 'Genres':
        fig = px.bar(lll, x=f'{column}', y='counts',
                     title=f'How many films per genre from which I have seen at least {min_} films between {year}-{year_}',
                     template='plotly_dark')

    return fig