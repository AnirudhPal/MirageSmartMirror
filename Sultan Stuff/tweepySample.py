import twitter

api = twitter.Api(consumer_key="NIubbVXjIABc8U9VeV49gZiDF",
                  consumer_secret="9U51pLaNgM6ytaU0aEiI53KXzNz9jgB6G2rrIAawMCuxUA5tb0",
                  access_token_key="1087968014-6LWAT8iz5GzVUrvqmFza7T26GPmpdQAPU5UhQbY",
                  access_token_secret="Drjj9NAVXLQCL4xBc2hZlsIv9UNbdUZddBsMLrQmfXFL1")
print(api.GetAppOnlyAuthToken(consumer_key="NIubbVXjIABc8U9VeV49gZiDF",
                  consumer_secret="9U51pLaNgM6ytaU0aEiI53KXzNz9jgB6G2rrIAawMCuxUA5tb0"))
statuses = api.GetHomeTimeline()
print([s.text for s in statuses])
