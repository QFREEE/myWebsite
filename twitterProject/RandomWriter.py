""" Based on final project in CS109 taught by Arther Peters"""

""" word, character,byte, none"""

import requests
import itertools
import pickle
from enum import Enum
from twitterProject.graph import Graph
import tweepy

class Tokenization(Enum):
    word = 1
    character = 2
    byte = 3
    none = 4


class RandomWriter(object):
    """A Markov chain based random data generator.
    """

    def __init__(self, level, tokenization=None):
        """Initialize a random writer.

        Args:
          level: The context length or "level" of model to build.
          tokenization: A value from Tokenization. This specifies how
            the data should be tokenized.

        The value given for tokenization will affect what types of
        data are supported.

        """
        self.graph = Graph()
        self.level = level
        self.tokenization = tokenization

    def generate(self):
        """Generate tokens using the model.

        Yield random tokens using the model. The generator should
        continue generating output indefinitely.

        It is possible for generation to get to a state that does not
        have any outgoing edges. You should handle this by selecting a
        new starting node at random and continuing.

        """
        current = None
        while True:
            node = self.graph.walkNode(current)
            current = node
            yield node[-1]

    def generate_tweets(self,amount):

      content = self.generate()
      content = zip(content, itertools.repeat(" "))
      content = itertools.chain.from_iterable(content)
      temp = itertools.islice(content,amount)
      tweet_str =""
      for i in list(temp):
        tweet_str+=(str(i))
      return tweet_str

    def generate_file(self, filename, amount):
        """Write a file using the model.

        Args:
          filename: The name of the file to write output to.
          amount: The number of tokens to write.

        For character or byte tokens this should just output the
        tokens one after another. For any other type of token a space
        should be added between tokens. Use str to convert values to
        strings for printing.

        Do not duplicate any code from generate.

        Make sure to open the file in the appropriate mode.
        """

        content = self.generate()
       
        if self.tokenization == Tokenization.byte:
            with open(filename, "wb") as fi:
              temp = itertools.islice(content,amount)
              fi.write(bytearray(temp))
    
        else:
            with open(filename, "wt", encoding="utf-8") as fi:
              if (
                    self.tokenization == Tokenization.word
                    or self.tokenization == Tokenization.none
                ): 
                content = zip(content, itertools.repeat(" "))
                content = itertools.chain.from_iterable(content)

              temp = itertools.islice(content,amount)
              for i in list(temp):
                fi.write(str(i))


    def save_pickle(self, filename_or_file_object):
        """Write this model out as a Python pickle.

        Args:
          filename_or_file_object: A filename or file object to write
            to. You need to support both.

        If the argument is a file object you can assume it is opened
        in binary mode.

        """
        try:
            pickle.dump(self, filename_or_file_object)
        except TypeError:
            with open(filename_or_file_object, "wb") as fi:
                pickle.dump(self, fi)

    @classmethod
    def load_pickle(cls, filename_or_file_object):
        """Load a Python pickle and make sure it is in fact a model.

        Args:
          filename_or_file_object: A filename or file object to load
            from. You need to support both.
        Return:
          A new instance of RandomWriter which contains the loaded
          data.

        If the argument is a file object you can assume it is opened
        in binary mode.

        """
        try:
            input = pickle.load(filename_or_file_object)
        except TypeError:
            with open(filename_or_file_object, "rb") as fi:
                input = pickle.load(fi)

        try:
            return cls(input.level, input.tokenization)
        except TypeError:
            raise ValueError("illeagl pickel loaded!")

    def train_url(self, url):
        """Compute the probabilities based on the data downloaded from url.

        Args:
          url: The URL to download. Support any URL supported by
            urllib.

        This method is only supported if the tokenization mode is not
        none.

        Do not duplicate any code from train_iterable.

        """
        if self.tokenization == Tokenization.none:
            raise ValueError("do NOT support none Tokenization")

        input = requests.get(url)
        input.encoding = "utf-8"
        if self.tokenization == Tokenization.byte:
            self.train_iterable(input.content)
        else:
            self.train_iterable(input.text)

     
    # TODO remove @ , http://  , retweet from each tweet
    def get_tweets(self,username):

      consumer_key = "pNFWoAS3k52wYqieWokrNlmH9" 
      consumer_secret = "1Da6e34YRkhsOFa9jLYDYkgutno9KQgsegXzsTVrO5pG25RTC2"
      access_key = "3301295378-RpwqbA5opPh5PusHwfwBcOBkXUgzyTnBmLCGdER"
      access_secret = "g5740xoRYMaIElUMBh6g9K43g8nTZI48P83gmp39ztC6g"

          
      # Authorization to consumer key and consumer secret 
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

      # Access to user's access key and access secret 
      auth.set_access_token(access_key, access_secret) 

      # Calling api 
      api = tweepy.API(auth) 

      # 200 tweets to be extracted 
      
      # tweets = api.user_timeline(screen_name=username) 

      #initialize a list to hold all the tweepy Tweets
      alltweets = []	
      
      #make initial request for most recent tweets (200 is the maximum allowed count)
      new_tweets = api.user_timeline(screen_name = username,count=200)
      
      #save most recent tweets
      alltweets.extend(new_tweets)
      
      #save the id of the oldest tweet less one
      oldest = alltweets[-1].id - 1
  
      #keep grabbing tweets until there are no tweets left to grab
      while len(new_tweets) > 0:
       

     
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name =username,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
       
 
      # yielding all the original tweet from user
      for tweet in alltweets:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
  
          yield tweet.text
    
    def clean_tweets(self,username):
      tweets = self.get_tweets(username)
      for tweet in tweets :
        wordList = tweet.split()
        for word in wordList:
          if word[0] != '@' and "https" not in word:
            yield word
    
    def train_tweets(self,username):
      temp = self.clean_tweets(username)
      self.train_iterable(temp)

    def train_iterable(self, data):
        """Compute the probabilities based on the data given.

        If the tokenization mode is none, data must be an iterable. If
        the tokenization mode is character or word, then data must be
        a string. Finally, if the tokenization mode is byte, then data
        must be a bytes. If the type is wrong raise TypeError.

        Try to avoid storing all that data at one time, but if it is way
        simpler to store it don't worry about it. For most input types
        you will not need to store it.
        """
        # HINT: You will find you need to convert the input iterable
        # into a new iterable. One step is already implemented in the
        # final_tests.py file. You may use that code (making sure to
        # give credit where credit is due). If you are wondering when
        # you need to convert iterables, remember how much I hate
        # indexing into lists and that not every iterable you get here
        # will support indexing.

        """ type checking"""
        if self.tokenization == Tokenization.character:
            if not isinstance(data, str):
                raise TypeError("data is not string")

        elif self.tokenization == Tokenization.word:
            if not isinstance(data, str):
                raise TypeError("data is not string")
            data = list(data.split())

        elif self.tokenization == Tokenization.byte:
            if not isinstance(data, bytes):
                raise TypeError("data is not bytes")
    
        elif self.tokenization == Tokenization.none:
            if not hasattr(data, "__iter__"):
                raise TypeError("data is not iterable")

        WINDOW_SIZE = self.level

        window = self.windowned(data, WINDOW_SIZE)  # this is a generator
        pre = None

        for node in window:
            self.graph.addEdge(node, pre)
            pre = node

   
    def windowned(self, data, size):
      """
      by Arther Peter
      produce a window generator on data
      """

      window = list()
      for v in data:
          if len(window) < size:
              window.append(v)
          else:
              window.pop(0)
              window.append(v)

          if len(window) == size:
              yield tuple(window)
      
    def train_txt(self,filename):
      data = None
      with open(filename,'r',encoding = 'utf-8') as fi:
        data = fi.read().replace('\n', '')

      self.train_iterable(data)



"""Modules you will want to look at:
* enum
* pickle
* requests

You may use the requests if you like even though it is not in the
standard library. I will make sure it is installed on the testing
machine.

"""

# TEST CODE
# import pprint

if __name__ == "__main__":
    r = RandomWriter(15, Tokenization.none)
    # r.train_iterable("asdfa sdfs adf")
    # for i in r.generate():
    #   print(i)
    # pprint.pprint(r.graph.__dict__)
    # r.generate_file("pride.txt", 500)
    r.train_tweets("BBC")
    r.generate_file("trump.txt",100)
