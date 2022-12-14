# Dataset
DATA_INPUT_DIR = "./datasets"
INPUT_FILE = DATA_INPUT_DIR + "/" + "1GB_file.txt"

# Input and output folders
OUTPUT_DIR = "./output_data"
INDEX_DIR = "./index"

# Regex
NAME_REGEX = r"<http:\/\/rdf\.freebase\.com\/ns\/[m]\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/type.object.(name)>\s+\"([^>]+)\"@en\s+\."
TYPE_REGEX = r"<http:\/\/rdf\.freebase\.com\/ns\/[m]\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/type\.object\.(type)>\s+<http:\/\/rdf\.freebase\.com\/ns\/([^>]+)>\s+\."
ALIAS_REGEX = r"<http:\/\/rdf\.freebase\.com\/ns\/[m]\.([^>]+)>\s+<http:\/\/rdf\.freebase\.com\/ns\/common.topic.(alias)>\s+\"([^>]+)\"@en\s+\."

# Searching
MAX_RESULTS = 20

# Testing
PRESENT_WORD = "music"
PRESENT_PHRASE = "Metal Militia - A Tribute to Metallica"
