from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))
 
assistant = client.beta.assistants.create(
  instructions="You are a social media assistant. Help users create and manage Twitter posts.",
  model="gpt-4",
  tools=[
    {
      "type": "function",
      "function": {
        "name": "create_tweet",
        "description": "Create and post a tweet",
        "parameters": {
          "type": "object",
          "properties": {
            "content": {
              "type": "string",
              "description": "The content of the tweet (max 280 characters)"
            },
            "hashtags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Optional hashtags to include in the tweet"
            }
          },
          "required": ["content"]
        }
      }
    },
    {
      "type": "function", 
      "function": {
        "name": "analyze_tweet_sentiment",
        "description": "Analyze the sentiment of a draft tweet",
        "parameters": {
          "type": "object",
          "properties": {
            "tweet_text": {
              "type": "string",
              "description": "The tweet text to analyze"
            }
          },
          "required": ["tweet_text"]
        }
      }
    }
  ]
)

def create_tweet(content, hashtags=[]):
    """
    Function to create and post a tweet
    """
    # Add hashtags to content if provided
    if hashtags:
        hashtag_text = " ".join([f"#{tag}" for tag in hashtags])
        content = f"{content} {hashtag_text}"
    
    # Here you would integrate with Twitter API
    # For demonstration, we'll just print the tweet
    print(f"Tweet created: {content}")
    return {"status": "success", "tweet": content}

def analyze_tweet_sentiment(tweet_text):
    """
    Function to analyze tweet sentiment
    """
    # Here you would integrate with a sentiment analysis service
    # For demonstration, we'll return a simple response
    return {
        "sentiment": "positive",
        "confidence": 0.8
    }

def get_user_input():
    """
    Get tweet content and optional hashtags from user
    """
    print("\n=== Twitter Post Creator ===")
    content = input("Enter your tweet content (max 280 chars): ")
    
    hashtags_input = input("Enter hashtags (comma-separated) or press Enter to skip: ")
    hashtags = [tag.strip() for tag in hashtags_input.split(",")] if hashtags_input else []
    
    return content, hashtags

def main():
    while True:
        content, hashtags = get_user_input()
        
        # Analyze sentiment before posting
        sentiment_result = analyze_tweet_sentiment(content)
        print(f"\nTweet Sentiment Analysis:")
        print(f"Sentiment: {sentiment_result['sentiment']}")
        print(f"Confidence: {sentiment_result['confidence']}")
        
        # Ask for confirmation
        confirm = input("\nWould you like to post this tweet? (y/n): ")
        if confirm.lower() == 'y':
            result = create_tweet(content, hashtags)
            print(f"\nStatus: {result['status']}")
        
        # Ask to continue
        continue_posting = input("\nWould you like to create another tweet? (y/n): ")
        if continue_posting.lower() != 'y':
            break

if __name__ == "__main__":
    main()

