from nltk.corpus import stopwords
import re
import nltk
import emoji

stopwords = stopwords.words('english')

twitch_system_words = { # Common Twitch system messages
    'welcome', 'joined', 'left', 'hosted', 'hosting',
    'subscribed', 'gifted', 'sub', 'prime', 'tier', 
    'months', 'streak', 'resubscribed', 'raided'
}

stopwords += list(twitch_system_words)

chat_filler_stopwords = {
    'lol', 'lmao', 'like', 'hai', 'mhm', 'yeah', 'yawn', 
    'bro', 'back', 'get', 'one', 'good', 'want', 'think', 
    'know', 'im', 'thats', 'dont', 'cant', 'tho', 'oh', 'uh',
    'ok', 'okay', 'right', 'maybe', 'well', 'see', 'bot',
    'watch', 'streams', 'turn', 'stop', 'please', 'got', 'ass', 'fire', 'call',
    'kekw', 'lul', 'pog', 'poggers', 'monka', 'ez', 'monkas', 'pepe', 'xd', 
    'omegalul', 'gasm', 'hi'

}

stopwords += list(chat_filler_stopwords)

# Define your spam phrases globally outside the functions
# Add any suspected bot/alert phrases confirmed from your investigation
SPAM_PHRASES = {
    'subscribed with prime', 
    'subscribed for',
    'just subscribed',
    'gifted a subscription', 
    'gifted a sub',
    'gifted sub',
    'gift',
    'donate',
    'consecutive streams'
}


def generate_alias_set(streamer_name):
    """
    Generates a set of potential aliases by simplifying the complex streamer name.
    """
    aliases = {streamer_name.lower()}
    
    # 1. Remove leading/trailing numbers and symbols (2xrakai -> rakai)
    # This targets names like 'Lirik123' or 'XqcOW'
    simple_name = re.sub(r'(\d+|tv|live|gaming|ow|hd|_|-)$', '', streamer_name, flags=re.IGNORECASE)
    simple_name = re.sub(r'^(\d+|tv|live|gaming|ow|hd|_|-)', '', simple_name, flags=re.IGNORECASE)

    if simple_name.lower() != streamer_name.lower() and len(simple_name) >= 3:
        aliases.add(simple_name.lower())
    
    # 2. Generate prefixes of the simplified name (rakai -> rak, raka, rakai)
    # This catches the original 'aceu' -> 'ace'
    if len(simple_name) >= 3:
        for i in range(3, len(simple_name) + 1):
            aliases.add(simple_name[:i].lower())
            
    # 3. Heuristic for complex names: The common short alias is often the last part.
    # This specifically targets 'rakai' -> 'kai'
    if len(simple_name) > 4:
        short_alias = simple_name[-3:].lower() # Take the last 3 characters
        if short_alias.isalpha(): # Only include if it's not just numbers/symbols
            aliases.add(short_alias)
            
    return aliases


def is_auto_message(text):
    """
    Checks if a message body contains known system/alert phrases.
    """
    lowered_text = text.lower()
    
    # Check for known system phrases
    for phrase in SPAM_PHRASES:
        if phrase in lowered_text:
            return True
            
    # Optional: Check for short, common non-human phrases 
    # (e.g., just 'hi' or 'xD' might pass this, but you can adjust)
    # if len(lowered_text.split()) < 2:
    #    return True 

    return False

def squash_spam(token):
    
    if len(token) > 2:
        # Check for 3 or more consecutive identical characters
        pattern = r'(.)\1{2,}'
        if re.search(pattern, token):
            return True


def remove_mentions(text):
    """
    Removes all user mentions (e.g., @MukkingAround, @OmegaTooYew) 
    from the text, replacing them with a space.
    """
    # Regex pattern: Looks for the '@' symbol followed by one or more 
    # non-whitespace characters, up to the end of the word/line.
    # It handles common Twitch names (which often include letters, numbers, and underscores).
    pattern = r'@\S+'
    return re.sub(pattern, ' ', text).strip()


def remove_streamer_name(text, streamer):
    if not streamer:
        return text

    aliases_to_remove = generate_alias_set(streamer)

    # Escape and sort by length descending
    escaped_aliases = [re.escape(alias) for alias in aliases_to_remove]
    escaped_aliases.sort(key=len, reverse=True)
    
    pattern_str = '|'.join(escaped_aliases)
    
    # Simple, high-impact substitution:
    cleaned_text = re.sub(pattern_str, " ", text, flags=re.IGNORECASE) 
    
    return cleaned_text

def normalize_urls(text):
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

def preprocess_text(text, streamer):

    text = normalize_urls(text)
    text = remove_mentions(text)
    text = remove_streamer_name(text, streamer)
    text = emoji.demojize(text, delimiters=(" ", " ")) # Reformat emojis to text
    lowered_text = text.lower()
    tokens = nltk.word_tokenize(lowered_text)
    tokens = [token for token in tokens if token.isalnum()] # Keep only alphanumeric tokens
    tokens = [token for token in tokens if not squash_spam(token)]
    tokens = [token for token in tokens if token not in stopwords]
    return tokens