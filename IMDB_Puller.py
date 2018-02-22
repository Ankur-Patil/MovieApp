# coding=utf-8

"""User will input title of movie into command line and movie ratings
will come up with reviews if requested"""

from imdbpie import Imdb


class Movie:
    """This movie class is provided the name and then pulls the title ID from IMDB database and then has a range
    of methods to provide the user information about the movie up to their choosing. None of the data is gathered until
    the user chooses, to reduce calls on the database."""

    def __init__(self, name):
        self.title = name
        self.ID = ""
        self._get_ID()  # Initializes with ID number
        self.rating = {}
        self.user_reviews = []
        self.summary = {}
        self.genre = {}
        self.similar = {}
        self.awards = {}

    def _get_ID(self):
        """Gets title from IMDB database and stores it in self.ID"""
        raw_data = imdb.search_for_title(self.title)
        if len(raw_data) > 1:
            raw_data = raw_data[0]  # Pulls the first value of the title (the closest match)
            # if there is more than one
        self.ID = raw_data['imdb_id']

    def get_rating(self):
        """Gets numerical rating from returned Rating dicitonary"""
        self.rating = imdb.get_title_ratings(self.ID)['rating']

    def get_user_reviews(self):
        """Gets dictionary of user reviews"""
        raw_review_data = imdb.get_title_user_reviews(self.ID)  # Returns dictionary of dicts
        reviews_dict = raw_review_data['reviews']  # Stores the dictionary of reviews
        for dictionary in reviews_dict:
            self.user_reviews.append(dictionary['reviewText'])
            # Appends review text to list
        self._review_printer()  # Calls printer to output reviews

    def _review_printer(self):
        """Prints out reviews, one at a time after confirmation to continue from user"""
        cont = input("Read a review? (y/n) ")
        if cont == 'y':
            review_count = len(self.user_reviews)
            for i in range(review_count):
                # Cycles through all reviews one at a time (amount is chosen by user)
                print('\n' + self.user_reviews[i])
                if i == (review_count - 1):
                    print('\nEnd of reviews.')
                    break
                cont = input("\nRead another review? (y/n) ")
                # Continues on if user says y, ceases if n
                if cont == 'n':
                    break

    def get_summary(self):
        """Gets summary data"""
        self.summary = imdb.get_title_plot(self.ID)

    def get_similarities(self):
        """Gets similarity data"""
        self.similar = imdb.get_title_similarities(self.ID)

    def get_genre(self):
        """Gets genre data then prints it using the _genre_printer method"""
        self.genre = imdb.get_title_genres(self.ID)
        self._genre_printer()

    def _genre_printer(self):
        """Prints out year and then genres"""
        print("Year: " + str(self.genre['year']))  # Prints out year
        print("Genre: " + ', '.join(self.genre['genres']) + "\n")  # Prints out genres

    def get_awards(self):
        """Extracts awards list of dictionaries"""
        self.awards = imdb.get_title_awards(self.ID)['awards']
        self._awards_parser()

    def _awards_parser(self):
        """Prints out the award won in which category and at what event if it won the award"""
        for award in self.awards:
            if award['isWinner']:
                print("Won " + award['awardName'] + " in the " + award['category'] +
                      " category at " + award['eventName'] + ".\n")


# Need to move all of this to another file to make it easier to Read

imdb = Imdb()  # Initialize Imdb Object
movie_name = input("Enter name of movie: ")
movie = Movie(movie_name)


def option_chooser():
    """Gives the option menu for the user to pick what information they want"""
    option_ = True
    choice = input("Do you want to find out information about " + movie_name + "? (y/n) ")
    if choice == "n":
        option_ = False
    return option_


go_on = True
while go_on:
    print("\n1. Rating\n2. Reviews\n3. Genre\n4. Awards\n")
    option = int(input("What do you want to see about " + movie.title + "? "))
    print()
    if option == 1:
        movie.get_rating()
        print(movie.rating)
        print()
        go_on = option_chooser()

    elif option == 2:
        movie.get_user_reviews()
        go_on = option_chooser()

    elif option == 3:
        movie.get_genre()
        go_on = option_chooser()

    elif option == 4:
        movie.get_awards()
        go_on = option_chooser()
