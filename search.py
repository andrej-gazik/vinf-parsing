from conf import INDEX_DIR, MAX_RESULTS
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import scoring
import json
import re


def result_str_no_id(result):
    if result.get("name"):
        return result.get("predicate") + " : " + result.get("name")

    if result.get("alias"):
        return result.get("predicate") + " : " + result.get("alias")

    if result.get("type"):
        return result.get("predicate") + " : " + result.get("type")


def result_data(result):
    if result.get("name"):
        return {
            "id": result.get("id"),
            "predicate": result.get("predicate"),
            "object": result.get("name"),
        }

    if result.get("alias"):
        return {
            "id": result.get("id"),
            "predicate": result.get("predicate"),
            "object": result.get("alias"),
        }

    if result.get("type"):
        return {
            "id": result.get("id"),
            "predicate": result.get("predicate"),
            "object": result.get("type"),
        }


def unique_results(results):

    unique = []

    for result in results:
        res = result_str_no_id(result)
        if res not in unique:
            unique.append(res)

    return unique


def print_results(results, s):

    qp_id = QueryParser("id", schema=i.schema)

    for index, result in enumerate(results, start=1):

        print(
            str(index)
            + " "
            + json.dumps(result_data(result), ensure_ascii=False)
            + "\t"
            + "Score: "
            + str(+round(result.score, 2))
        )

        q = qp_id.parse(result.get("id"))
        for r in unique_results(s.search(q)):
            print("\t\t" + r)

    print("---------------------------------")


def search(query, i, s):
    match = re.search('"(.*?)"', query)

    qp_multi = MultifieldParser(["name", "alias", "type"], schema=i.schema)

    if match is not None:
        q = qp_multi.parse("'" + query + "'")
    else:
        q = qp_multi.parse(query)

    return s.search(q, limit=MAX_RESULTS)


if __name__ == "__main__":

    i = index.open_dir(INDEX_DIR)
    s = i.searcher(weighting=scoring.TF_IDF())

    while True:
        print("Input phrase to search:")
        input_query = input("input query: ")

        results = search(input_query, i, s)

        print("Results for: " + input_query)
        print_results(results, s)
