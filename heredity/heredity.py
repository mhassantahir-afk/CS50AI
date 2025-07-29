import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                'mother': row['mother'] or None,
                'father': row['father'] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    result = 1.000  # this is initialization of result that will be changed in the logic below and then returned

    zero_gene = set()
    for person in people:  # loop runs on people and adds all of the people with no mutated gene listed
        if person not in one_gene and person not in two_genes:
            zero_gene.add(person)

    for person in people:
        # for people who have no parents listed
        if people[person]['father'] is None and people[person]['mother'] is None:
            gene_number = -1  # initialization of gene_number with random non possible probability
            if person in zero_gene:  # to check if they have any mutated gene(1, 2, 0)
                result *= PROBS["gene"][0]
                gene_number = 0
            elif person in one_gene:
                result *= PROBS["gene"][1]
                gene_number = 1
            elif person in two_genes:
                result *= PROBS["gene"][2]
                gene_number = 2

            if person in have_trait:  # to check if trait is listed as true or not in the dict
                result *= PROBS["trait"][gene_number][True]
            else:
                result *= PROBS["trait"][gene_number][False]

            '''
                the probabilities are multiplied by the gene number to the specific trait present
                this changes the probabilities based on the conclusion deducted from the data given
            '''

        elif people[person]['father'] != None and people[person]['mother'] != None:
            # the 'p' in these variables stand for probability, (-1) is initialization place holder
            pmother = -1  # this is the probability of the mother
            pfather = -1  # this is the probability of the father
            ptransfer = -1  # this is the probability of the transfer
            gene_number = -1  # this gene_number will be modified in the logic below

            '''
                if one gene is present then mother & father contribute half(0.5) equating to full(1)
                if two genes are present then the probability is the difference of 1 and mutation probability
                (meaning 1 - 0.01 = 0.99 thus 99% probability that the gene remains unchanged)
                if no gene is present then the probability of mutation is the original probability of mutation(chance) from PROBS
            '''

            if people[person]['mother'] in one_gene:
                pmother = 0.5
            elif people[person]['mother'] in two_genes:
                pmother = 1 - PROBS["mutation"]
            else:
                pmother = PROBS["mutation"]

            if people[person]['father'] in one_gene:
                pfather = 0.5
            elif people[person]['father'] in two_genes:
                pfather = 1 - PROBS["mutation"]
            else:
                pfather = PROBS["mutation"]

            '''
                (genes in children)
                if no genes are present then the probability of transfer is low and equates to the joint probability(product) of the differences of father and mother genes
                if one gene is present then the probability of transfer is the disjoint probability(sum) as written below
                if two genes are present then the probability of transfer is the joint probability(product) of the pmother and pfather
            '''

            if person in zero_gene:
                ptransfer = (1-pmother) * (1-pfather)
                gene_number = 0
            elif person in one_gene:
                ptransfer = pmother * (1-pfather) + pfather * (1-pmother)
                gene_number = 1
            elif person in two_genes:
                ptransfer = pmother * pfather
                gene_number = 2

            result *= ptransfer  # result is modified

            if person in have_trait:  # changes based upon the number of genes and if the child shows trait or not
                result *= PROBS["trait"][gene_number][True]
            else:
                result *= PROBS["trait"][gene_number][False]

    return result  # returns result after modification


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities.keys():  # loop iterates over all of the people
        if person in one_gene:  # if the person has one gene then the probability of that person's one gene increases by the joint probability 'p'
            probabilities[person]['gene'][1] += p
        elif person in two_genes:  # if the person has two genes then the probability of that person's two genes increases by the joint probability 'p'
            probabilities[person]['gene'][2] += p
        else:  # if there is no gene then the zero gene probability increases by 'p'
            probabilities[person]['gene'][0] += p

        if person in have_trait:  # if person shows trait then we add 'p' into the trait True probability
            probabilities[person]['trait'][True] += p
        else:  # if person does not show trait then we add 'p' into the trait False probability
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities.keys():
        genes = probabilities[person]["gene"]
        traits = probabilities[person]["trait"]

        gene_sum = 0
        trait_sum = 0

        # trait sum is increased by the probability of the traits in True and False
        trait_sum += traits[True]
        trait_sum += traits[False]

        # we add joint probability(product) of the trait sum
        probabilities[person]['trait'][True] *= 1 / trait_sum
        probabilities[person]['trait'][False] *= 1 / trait_sum

        # adds the gene_sum for all of the genes present in probabilities
        for i in range(3):
            gene_sum += genes[i]

         # adds the gene_sum joint probability(product) into probabilities
        for i in range(3):
            probabilities[person]['gene'][i] *= 1 / gene_sum


if __name__ == "__main__":
    main()
