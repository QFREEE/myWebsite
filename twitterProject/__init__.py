""" from twitter handleing only"""
import twitterProject.RandomWriter as RW

LEVEL = 15
def twitterGenerator(username):
    R = RW.RandomWriter(15)
    R.train_tweets(username)
    result = R.generate_tweets(100)
    return result