import csv
from collections import defaultdict, namedtuple, OrderedDict

MOVIE_DATA = 'movie_metadata.csv'
NUM_TOP_DIRECTORS = 20
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    '''Extracts all movies from csv and stores them in a dictionary
    where keys are directors, and values is a list of movies (named tuples)'''
    directors = defaultdict(list)

    with open(MOVIE_DATA, encoding='utf-8') as f:
        for m in csv.DictReader(f):
            try:
                mm = Movie(title=m['movie_title'].strip(), year=int(m['title_year']), score=float(m['imdb_score']))
                if mm.year < MIN_YEAR:
                    continue
                directors[m['director_name']].append(mm)
            except Exception as ex:
                #print(m)
                pass

    return directors


def get_average_scores(directors):
    '''Filter directors with < MIN_MOVIES and calculate averge score'''
    directors_ext = OrderedDict()
    for d in directors:
        movies = directors[d]
        counter = len(movies)
        if counter < MIN_MOVIES:
            continue
        avg = _calc_mean(movies)
        directors_ext[(d, avg)] = movies
    return directors_ext


def _calc_mean(movies):
    '''Helper method to calculate mean of list of Movie namedtuples'''
    ml = len(movies)
    avg = round(sum([mm.score for mm in movies])/ml, 1)
    return avg


def print_results(directors):
    '''Print directors ordered by highest average rating. For each director
    print his/her movies also ordered by highest rated movie.
    See http://pybit.es/codechallenge13.html for example output'''
    fmt_director_entry = '{counter}. {director:<53} {avg}'
    fmt_movie_entry = '{year}] {title:<50} {score}'
    sep_line = '-' * 60

    top_directors = sorted(directors.items(), key=lambda d: d[0][1], reverse=True)[:20]

    for de in top_directors:
        print(fmt_director_entry.format(counter=len(de[1]), director=de[0][0], avg=de[0][1]))
        top_movies = sorted(de[1], key=lambda mv: mv.score, reverse=True)
        print(sep_line)
        for mm in top_movies:
            print(fmt_movie_entry.format(year=mm.year, title=mm.title, score=mm.score))
        print()


def main():
    '''This is a template, feel free to structure your code differently.
    We wrote some tests based on our solution: test_directors.py'''
    directors = get_movies_by_director()
    directors = get_average_scores(directors)
    print_results(directors)


if __name__ == '__main__':
    main()
