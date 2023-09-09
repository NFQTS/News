import json
class Source:
    source_id_counter = 1  # Class-level variable to track source IDs

    def __init__(self, name, stories, rankings):
        self.id = Source.get_next_id()  # Assign a unique ID
        self.name = name
        self.stories = stories
        self.rankings = rankings

    @classmethod
    def get_next_id(cls):
        current_id = cls.source_id_counter
        cls.source_id_counter += 1
        return current_id

class Story:
    story_id_counter = 1
    
    def __init__(self, headline, content, author, source, date, ranking):
        self.id = Story.get_next_id()
        self.headline = headline
        self.content = content
        self.author = author
        self.source = source
        self.date = date
        self.ranking = ranking

    @classmethod
    def get_next_id(cls):
        current_id = cls.story_id_counter
        cls.story_id_counter += 1
        return current_id

class SourceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Source):
            # Convert a Source instance to a dictionary for serialization
            return {
                'id': obj.id,
                'name': obj.name,
                'stories': obj.stories,
                'rankings': obj.rankings
            }
        return super().default(obj)