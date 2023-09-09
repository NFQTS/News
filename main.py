import functions as f

def main(): 
    #f.fetch_news()
    f.preprocess_news_data()
    # f.NeuralNetworkModel()
    f.distribute_news()
    f.collect_user_feedback()
main()