import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    no_of_pages = len(corpus)

    # this will make a dictionary with keys from the corpus and set their initial values as (1-d/N)
    probability_distribution = {key: (1-damping_factor)/no_of_pages for key in corpus}

    links = corpus[page]  # retreives the links attached in the page given

    if links:  # if the page has any links
        # for loop runs over all of the links and puts the value of those pages by adding with (d/N)
        for linked_page in links:
            probability_distribution[linked_page] += (damping_factor / len(links))
    else:  # if the page has no links then all of the pages have the (1/N) probability
        for p in corpus:
            probability_distribution[p] = (1/no_of_pages)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    Pagerank = {key: 0 for key in corpus}  # making a new dictionary with 0 values as for everypage

    page = random.choice(list(Pagerank.keys()))  # selects a random page for starting

    # adds the no of visits to the page, since the page is visited once already it is manually added by 1
    Pagerank[page] += 1

    for i in range(n):  # runs for the number of SAMPLES
        # this will return a dictionary for the amount of probabilities for each page
        distribution = transition_model(corpus, page, damping_factor)

        ''' this uses random.choices() to randomly choose from the pages with corresponding probabilites
            it makes a dictionary that has keys as the pages and weights(probability) and choice as k=1(meaning only one can be selected)
            this will select any random one of the pages using the probabilites they come with
            (higher the probabilty higher is the chance of selection)'''
        page = random.choices(
            list(distribution.keys()),
            weights=list(distribution.values()),
            k=1
        )[0]

        Pagerank[page] += 1  # the page is taken and marked as a visit

    for point in Pagerank:  # for loop iterates over all of the pages and divides their values by the sampling number
        Pagerank[point] /= n

    return Pagerank  # returns the final probability ranking


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    no_of_pages = len(corpus)

    # makes a dictionary that has keys of the corpus and initial value as (1/N)
    Pagerank = {key: 1/no_of_pages for key in corpus}
    Pagerank2 = Pagerank.copy()  # make an additional dictionary so we can compare the values

    loop_setup = True  # for using in the while loop

    while (loop_setup):
        for page in corpus:  # for loop takes page from corpus one by one
            summation = 0.000  # this is the sigma from the formula given
            for page2 in corpus:  # inner loop takes each page

                # this condition check if the inner loop page2 has some links in it and if the first page is present in the page2 links
                if (corpus[page2]) and (page in corpus[page2]):
                    # this adds the summation with the probabilty of page2 divided by number of links in it
                    summation += Pagerank[page2]/len(corpus[page2])
                # if no links are present in page2 then we simply add the summation with probability of page2 divited by the Number of pages
                elif not corpus[page2]:
                    summation += Pagerank[page2]/len(corpus)

            # this is the final PR(p) of the formula
            Pagerank2[page] = ((1 - damping_factor)/len(corpus) + damping_factor * summation)

        # after one run of the outer loop we check if the difference of the two ranks is less than 0.001
        if all(abs(Pagerank2[page] - Pagerank[page]) < 0.001 for page in Pagerank):
            loop_setup = False

        Pagerank = Pagerank2.copy()

    return Pagerank


if __name__ == "__main__":
    main()
