import json
import sqlite3
import flask

app = flask.Flask(__name__)


def get_value_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        result = connection.execute(sql).fetchall()

        return result


def search_by_title(title):
    sql = f"""
        SELECT *
        FROM netflix
        WHERE title = '{title}'
        ORDER BY release_year DESC
        LIMIT 1
            """
    result = get_value_from_db(sql)
    for item in result:
        return item


@app.get("/movie/<title>/")
def search_by_title_view(title):
    result = search_by_title(title=title)
    print(result)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
    )


@app.get("/movie/<year1>/to/<year2>/")
def search_date_view(year1, year2):
    sql = f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {year1} AND {year2}
        LIMIT 100
            """
    result = []
    for item in get_value_from_db(sql=sql):
        result.append(item)

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
    )


@app.get("/rating/<rating>/")
def search_rating_view(rating):
    my_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f"""
           SELECT title, rating, description
           FROM netflix
           WHERE rating in {my_dict.get(rating, ("R", "R"))}
               """

    result = []
    for item in get_value_from_db(sql=sql):
        result.append(item)

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
    )


@app.get("/genre/<genre>/")
def search_genre_view(genre):
    sql = f"""
              SELECT *
              FROM netflix
              WHERE listed_in like '%{genre}'
              ORDER BY release_year DESC
              LIMIT 10
              """

    result = []
    for item in get_value_from_db(sql=sql):
        result.append(item)

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
    )


def search_double_name(name1, name2):
    sql = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" like '%{name1}%' AND "cast" like '%{name2}%'
            """

    result = get_value_from_db(sql)
    all_names = []
    for item in result:
        for i in item:
            all_names += i.split(", ")

    double_names = []
    for item in all_names:
        if item != name1 and item != name2:
            if all_names.count(item) > 2:
                double_names.append(item)

    return set(double_names)


def step_6(typ, year, genre):
    sql = f"""
            SELECT title, description, listed_in
            FROM netflix
            WHERE type = '{typ}'
            AND release_year = '{year}'
            AND listed_in like '{genre}'
            """
    result = []
    for item in get_value_from_db(sql):
        result.append(item)
    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app.run(debug=True)
