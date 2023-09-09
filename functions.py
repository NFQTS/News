import json, requests, os, time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import classes as c

DATA_DIR = "news_data"
API_KEY = os.environ["news_api"]
NEWS_SOURCES = [
    'cnn', 'abc-news', 'google-news', 'the-new-york-times', 'cbs-news',
    'associated-press', 'bbc-news', 'bloomberg', 'fox-news', 'msnbc',
    'newsweek', 'reuters', 'usa-today', 'wired', 'techcrunch'
]  # Add more sources as needed
# NEWS_SOURCES = [
#     'cnn', 'abc-news'
# ]  # Add more sources as needed
# Rate limit information
REQUESTS_PER_DAY = 95
REQUESTS_INTERVAL = 24 * 60 * 60 / REQUESTS_PER_DAY * len(NEWS_SOURCES)  # Interval in seconds

active_sources = []
headlines_processed = []
source_data = {}
X = []
y = []
def save_responses(data_list, filename):
    with open(filename, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)


def load_responses(filename):
    with open(filename, 'r') as json_file:
        data_list = json.load(json_file)
        return data_list

def fetch_news():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    responses_filename = os.path.join(DATA_DIR, 'last_news_query.json')
    
    try:
        saved_responses = load_responses(responses_filename)
        print("Loaded saved responses.")
    except FileNotFoundError:
        saved_responses = []

    for source in NEWS_SOURCES:       
        fetched_responses = fetch_headlines(source)
        saved_responses.extend(fetched_responses)
        save_responses(saved_responses, responses_filename)
        
def fetch_headlines(source):
    url = f'https://newsapi.org/v2/top-headlines?sources={source}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    #print(data)
    if response.status_code == 200 and data['status'] == 'ok':
        return data['articles']
    else:
        print(f"Error fetching news from {source}")
        return []
def get_news_data():
    json_filename = 'news_data/last_news_query.json'
    with open(json_filename, 'r') as json_file:
        json_text = json_file.read()
        json_data = json.loads(json_text)
        #print(json_data)
        return json_data


def create_source(name):
    new_source = c.Source(name, {}, [])
    active_sources.append(name)
    source_data[new_source.id] = new_source

def rank_articles(text):
    ranking = input(f'Rank Article - {text}: ')
    if ranking == "1":
        print(1)
    elif ranking == "2":
        print(2)
    else:
        print("Please enter either a 1 or a 2.")
        rank_articles(text)
    return ranking

def save_source_data(data_dict, filename):
    with open(filename, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4, cls=c.SourceEncoder)

def preprocess_news_data():
    news_json = get_news_data()
    for story in news_json:
    # check if the headline has been used before.
    # print(story['title'])
        if story['title'] not in headlines_processed:
            print("New headline")
            headlines_processed.append(story['title'])
            headline = story['title']
            content = story['description']
            author = story['author']
            source = story['source']['id']
            date = story['publishedAt']
            ranking = 0
            new_story = c.Story(headline, content, author, source, date, ranking)
            print("New story created")
            if source not in active_sources:
                print("New source detected, adding it to the system.")
                create_source(source)
            # need to get some kind of source id mapping for the source names?
            print("Rank this article as 1 or 2. 1 = spam, 2 = relevant")
            article_ranking = rank_articles(new_story.headline)
            new_story.ranking = int(article_ranking)
            for outlet in source_data:
                print(outlet)
                print(source_data[outlet])
                if source_data[outlet].name == source:
                    source_data[outlet].stories[headline] = article_ranking
                    print(f'{source_data[outlet].name} updated with new story')
                    print(source_data)
                    source_data[outlet].rankings.append(int(article_ranking))
                else:
                    print("Problem")
                    print(source_data)
            print(new_story.headline, new_story.ranking)
    save_source_data(source_data, 'source_data.json')

def NeuralNetworkModel():
    json_file = "source_data.json"

    try:
        with open(json_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File '{json_file}' not found.")
        exit(1)
    
    # Extract headlines and rankings from the loaded data
    for source_id, source_data in data.items():
        if "stories" in source_data:
            for headline, ranking in source_data["stories"].items():
                X.append(headline)
                y.append(int(ranking))
        else:
            print(f"Invalid data format in the JSON file. Each source should have a 'stories' field.")
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Text vectorization
    vectorizer = CountVectorizer(max_features=1000)  # You can adjust the number of features as needed
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Create and train a neural network model (MLPClassifier in this example)
    model = MLPClassifier(hidden_layer_sizes=(420, 69), max_iter=2000, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Predict rankings for new headlines
    new_headlines = ["Trump is arrested.", "Biden may have trouble soon.", "Hurricane hits Florida."]
    new_headlines_vec = vectorizer.transform(new_headlines)
    predictions = model.predict(new_headlines_vec)
    
    # Print the predicted rankings
    for headline, prediction in zip(new_headlines, predictions):
        print(f"Headline: {headline}, Predicted Ranking: {prediction}")       

def distribute_news():
    pass

def collect_user_feedback():
    pass