import re
from fack.models import Question
from django.conf import settings


class conf:
    """
    Special sub namespace to define some specific configurations for the help functionality
    """
    # How many entries to show in the "most frequently asked questions" section.
    NR_TOP_QUESTIONS = getattr(settings, 'HELP_NR_TOP_QUESTIONS', 10)

    # How many entries to show in the "most viewed categories" section.
    NR_TOP_CATEGORIES = getattr(settings, 'HELP_NR_TOP_CATEGORIES', 6)

    # Defines how we determine top questions/topics.
    TOP_ORDER = getattr(settings, 'HELP_TOP_ORDER', ('-sort_order', '-nr_views',))

    # Maximum number of results to show on search page.
    MAX_SEARCH_RESULTS = getattr(settings, 'HELP_MAX_SEARCH_RESULTS', 20)

    # Minimum number of characters in the search query.
    MIN_SEARCH_QUERY_LEN = getattr(settings, 'HELP_MIN_SEARCH_QUERY_LEN', 3)

    # Number of characters to use for the context of a match in a search result.
    MATCH_CONTEXT_LEN = getattr(settings, 'HELP_MATCH_CONTEXT_LEN', 100)


def search(search_query):
    """
    Searches through the FAQ

    :param search_query: a query string to search the FAQ
    :return: a dict with the results and parsed words
    """
    min_query_len = conf.MIN_SEARCH_QUERY_LEN
    max_results = conf.MAX_SEARCH_RESULTS

    #query = request.GET.get('query', '').strip()
    query = search_query.strip()
    words = [w for w in query.split() if len(w) >= min_query_len]

    if not query:
        return None

    if len(query) >= min_query_len and words:
        # Search in the question as well as in the answer.
        try:
            # Try to import 'datatrans' to check if it is installed or not
            import datatrans

            q1 = Question.site_objects\
                .datatrans_filter(text__icontains=words).filter(status=Question.ACTIVE)\
                .order_by(*conf.TOP_ORDER)[:max_results]

            q2 = Question.site_objects\
                .datatrans_filter(answer__icontains=words).filter(status=Question.ACTIVE)\
                .order_by(*conf.TOP_ORDER)[:max_results]
        except:
            q1 = Question.site_objects.filter(text__icontains=query).filter(status=Question.ACTIVE)\
                .order_by(*conf.TOP_ORDER)[:max_results]

            q2 = Question.site_objects.filter(answer__icontains=query).filter(status=Question.ACTIVE)\
                .order_by(*conf.TOP_ORDER)[:max_results]

        questions = set(q1).union(q2)
        questions = sorted(questions, key=lambda q: q.nr_views, reverse=True)
        questions = questions[:max_results]
    else:
        questions = []

    def make_summary(text, words, context_len):
        """
        Extract part of the first sentence of the text that contains one of
        the given words. If we don't find a match, use the first one.
        """
        ellipsis = "\u2026"
        pattern = '|'.join(re.escape(w) for w in words)
        match = re.search(pattern, text, re.I)

        if match:
            start = max(0, match.start() - context_len // 2)
            end = min(len(text), match.end() + context_len // 2)
        else:
            start = 0
            end = context_len

        summary = text[start:end]

        if start > 0:
            summary = ellipsis + summary
        if end < len(text):
            summary += ellipsis

        return summary

    for question in questions:
        question.summary = make_summary(question.answer, words, conf.MATCH_CONTEXT_LEN)

    return {
        'questions': questions,
        'query': query,
        'words': words,
        'min_query_len': min_query_len,
    }
