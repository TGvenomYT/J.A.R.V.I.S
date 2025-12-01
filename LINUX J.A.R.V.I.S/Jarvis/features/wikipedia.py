import wikipedia
import re

def tell_me_about(topic):
    try:
        # Search for the topic first to get the most likely page title
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"Sorry, I couldn't find anything on Wikipedia for '{topic}'."
        
        # Use the first search result to get the summary
        page_title = search_results[0]
        summary = wikipedia.summary(page_title, sentences=3)
        return summary
    except Exception as e:
        print(f"An unexpected error occurred with Wikipedia search for '{topic}': {e}")
        return f"Sorry, I ran into an error trying to look up '{topic}' on Wikipedia."
