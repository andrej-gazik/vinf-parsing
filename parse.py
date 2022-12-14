from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from conf import *
import re
from conf import TYPE_REGEX, NAME_REGEX, ALIAS_REGEX


def get_matches(reg, row):
    # print("test")
    # print(row)
    res = list(re.findall(reg, row))
    if res:
        # print(res)
        res = list(res[0])[1:]
        return list(filter(None, res))
    else:
        return None


def match_patterns(s):

    # regex patterns to match
    patterns = [NAME_REGEX, ALIAS_REGEX, TYPE_REGEX]

    # Retrieve patterns or return None
    for pattern in patterns:
        matches = re.finditer(pattern, s)
        for matchNum, match in enumerate(matches, start=1):
            if len(match.groups()) > 0:
                # return json.dumps(
                #     {
                #         "subject_id": match.group(1),
                #         "predicate": match.group(2),
                #         "object": match.group(3),
                #     },
                #     ensure_ascii=False,
                # ).encode("utf8")
                return (match.group(1), match.group(2), match.group(3))


# def parse_triplets(row):

#     print(str(row))
#     # reg = r"(Row\(text='<http:\/\/rdf\.freebase\.com\/ns\/m\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/(type.object.type)>\s+<http:\/\/rdf\.freebase\.com\/ns\/([^>]+)>\s+\.|<http:\/\/rdf\.freebase\.com\/ns\/m\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/(type.object.name)>\s+\"([^>]+)\"@en\s+\.|<http:\/\/rdf\.freebase\.com\/ns\/m\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/(common.topic.alias)>\s+\"([^>]+)\"@en\s+\.\)')"

#     reg = r"(<http:\/\/rdf\.freebase\.com\/ns\/m\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/(type.object.type)>\s+<http:\/\/rdf\.freebase\.com\/ns\/([^>]+)>\s+\.|<http:\/\/rdf\.freebase\.com\/ns\/m\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/(type.object.name)>\s+\"([^>]+)\"@en\s+\.|<http:\/\/rdf\.freebase\.com\/ns\/m\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/(common.topic.alias)>\s+\"([^>]+)\"@en\s+\.)"
#     res = get_matches(reg, row)
#     if res:
#         # return {"id": res[0], "attribute": res[1], "data": res[2]}


config = SparkConf().setAll(
    [
        ("spark.executor.memory", "8g"),
        ("spark.executor.cores", "4"),
        ("spark.cores.max", "4"),
        ("spark.driver.memory", "8g"),
    ]
)


sc = SparkContext("local[*]", "PySpark Read JSON")

spark = SparkSession.builder.master("local[*]").appName("freebase_parser").getOrCreate()

# Load text file of RDF tripplets
f = sc.textFile(INPUT_FILE)

# Parse data via regex filter None and remove duplicates
rdd = f.map(lambda x: match_patterns(x)).filter(lambda x: x != None).distinct()

columns = ["subject_id", "predicate", "object"]

# Convert RDD into Spark DF
df = rdd.toDF(columns)

df.printSchema()
df.show(truncate=False)

# Output into parquet
df.write.mode("overwrite").parquet(OUTPUT_DIR)

# Save RDD into textfiles
# rdd.saveAsTextFile("./out")
