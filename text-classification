# https://googlecoursera.qwiklabs.com/focuses/46790 

Create api key in gcp

Create environment variabel 
export API_KEY=<YOUR_API_KEY>

Create a new file named request.json and add the following:

{
  "document":{
    "type":"PLAIN_TEXT",
    "content":"A Smoky Lobster Salad With a Tapa Twist. This spin on the Spanish pulpo a la gallega skips the octopus, but keeps the sea salt, olive oil, pimentón and boiled potatoes."
  }
}

Classify the text 
curl "https://language.googleapis.com/v1/documents:classifyText?key=${API_KEY}" \
  -s -X POST -H "Content-Type: application/json" --data-binary @request.json

To see the type of text you'll be working with, run the following command to view one article (gsutil provides a command line interface for Cloud Storage):
gsutil cat gs://text-classification-codelab/bbc_dataset/entertainment/001.txt
Create bigquery dataset and table
For Name, type news_classification_dataset
Click Create dataset.
Click on the name of the dataset, then select Create table. Use the following settings for the new table:
Create From: empty table
Name your table article_data
Click Add Field and add the following 3 fields: article_text, category, and confidence
First, back in Cloud Shell, export the name of your Cloud project as an environment variable. Replace <your_project_name> with the GCP Project ID found in the CONNECTION DETAILS section of the lab:
export PROJECT=<your_project_name>
Then run the following commands from Cloud Shell to create a service account:
gcloud iam service-accounts create my-account --display-name my-account
gcloud projects add-iam-policy-binding $PROJECT --member=serviceAccount:my-account@$PROJECT.iam.gserviceaccount.com --role=roles/bigquery.admin
gcloud iam service-accounts keys create key.json --iam-account=my-account@$PROJECT.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=key.json
Create a file called classify-text.py and copy the following into it. Replace YOUR_PROJECT with your GCP Project ID.
 
from google.cloud import storage, language, bigquery
 
# Set up our GCS, NL, and BigQuery clients
storage_client = storage.Client()
nl_client = language.LanguageServiceClient()
# TODO: replace YOUR_PROJECT with your project id below
bq_client = bigquery.Client(project='YOUR_PROJECT')
 
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
 
rows_for_bq = []
files = storage_client.bucket('text-classification-codelab').list_blobs()
print("Got article files from GCS, sending them to the NL API (this will take ~2 minutes)...")
 
# Send files to the NL API and save the result to send to BigQuery
for file in files:
        if file.name.endswith('txt'):
                article_text = file.download_as_string()
                nl_response = classify_text(article_text)
                if len(nl_response.categories) > 0:
                        rows_for_bq.append((str(article_text), str(nl_response.categories[0].name), str(nl_response.categories[0].confidence)))
 
print("Writing NL API article data to BigQuery...")
# Write article text + category data to BQ
errors = bq_client.insert_rows(table, rows_for_bq)
assert errors == []
 
python3 classify-text.py
Note: If you get an error while executing python3 classify-text.py, it might be the case the cloud shell get disconnected. In order to fix that, please export your environment variables by running the below commands then re-run the python3 classify-text.py command. export PROJECT= (GCP PROJECT ID) export GOOGLE_APPLICATION_CRTEDENTIALS=key.json
We're using the google-cloud Python client library to access Cloud Storage, the Natural Language API, and BigQuery. First, a client is created for each service; then references are created to the BigQuery table. files is a reference to each of the BBC dataset files in the public bucket. We iterate through these files, download the articles as strings, and send each one to the Natural Language API in our classify_text function. For all articles where the Natural Language API returns a category, the article and its category data are saved to a rows_for_bq list. When classifying each article is done, the data is inserted into BigQuery using insert_rows().
 
 

