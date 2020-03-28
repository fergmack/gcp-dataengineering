# from the Google Cloud Python client library, access Storage, NL API, and BigQuery
from google.cloud import storage, language, bigquery

# Set up our GCS, NL, and BigQuery clients
storage_client = storage.Client()
nl_client = language.LanguageServiceClient()
# TODO: replace YOUR_PROJECT with your project id below
bq_client = bigquery.Client(project='YOUR_PROJECT')

# access the dataset you've created in BQ
# look into these steps: seems to be
# 1) access the dataset via bq_client and store it in a dataset_ref variable
# 2) pass dataset_ref to BQ and store it in a dataset variable
# 3) acess the table article_data and store it in a table_ref variable
# 4) pass the table_ref to the bq_cleint and store in a table variable
dataset_ref = bq_client.dataset('news_classification_dataset')
dataset = bigquery.Dataset(dataset_ref)
table_ref = dataset.table('article_data') # Update this if you used a different table name
table = bq_client.get_table(table_ref)

# Send article text to the NL API's classifyText method
def classify_text(article):
        response = nl_client.classify_text(
                document=language.types.Document(
                        content=article,
                        type=language.enums.Document.Type.PLAIN_TEXT
                )
        )
        return response

# files variabel is a reference to the article text dataset
# get these from Cloud Storage
rows_for_bq = []
# Storage instance
files = storage_client.bucket('text-classification-codelab').list_blobs()
print("Got article files from GCS, sending them to the NL API (this will take ~2 minutes)...")

# Send files to the NL API and save the result to send to BigQuery
# iterate through each article in files
for file in files:
        if file.name.endswith('txt'):
                # file is the Storage instance created above so we can use download_as_string() method to dl
                article_text = file.download_as_string()
                # use the classify_text() function we created above. pass it the single article text we're currently on in this loop (file)
                nl_response = classify_text(article_text)
                # if the text has been categorised (i.e. sting > 0), write it to bq
                if len(nl_response.categories) > 0:
                        # note .categories[0].name gets first category
                        rows_for_bq.append((str(article_text), str(nl_response.categories[0].name), str(nl_response.categories[0].confidence)))

print("Writing NL API article data to BigQuery...")
# Write article text + category data to BQ
# insert it to the table we crated in step 4) above at the start
errors = bq_client.insert_rows(table, rows_for_bq)
# assert tests a condition 
assert errors == []
