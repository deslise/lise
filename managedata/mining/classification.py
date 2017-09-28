
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class AnalyzeVader(object):

    def polarity(self, frase):
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(frase)
        if vs['neg']>vs['pos']:
            return -1
        elif vs['pos']>vs['neg']:
            return 1
        else:
            return 0