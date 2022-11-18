from flask import Flask, render_template, request
from IPython.display import HTML
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import pandas as pd
from sentence_transformers import SentenceTransformer
import pinecone
import matplotlib.pyplot as plt
# Load dataset to a pandas dataframe
df = pd.read_csv(
     "gifdata.tsv",
    delimiter="\t",
    names=['pattern','responses']
)
df.to_csv('GfG1.csv',index=False)


# Connect to pinecone environment
pinecone.init(
    api_key="8d312ebd-f0c3-4e8f-af86-ef544975b895",
    environment="us-west1-gcp"
)

index_name = 'gif-responses'

# check if the gif-search exists
if index_name not in pinecone.list_indexes():
    # create the index if it does not exist
    pinecone.create_index(
        index_name,
        dimension=384,
        metric="cosine"
    )
# Connect to gif-search index we created
index = pinecone.Index(index_name)

# Initialize retriever with SentenceTransformer model
retriever = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
retriever

from tqdm.auto import tqdm

# we will use batches of 4
batch_size = 4

for i in tqdm(range(0, len(df), batch_size)):
    # find end of batch
    i_end = min(i + batch_size, len(df))
    # extract batch
    batch = df.iloc[i:i_end]
    # generate embeddings for batch
    emb = retriever.encode(batch['pattern'].tolist()).tolist()
    # get metadata
    meta = batch.to_dict(orient='records')

    # create IDs
    ids = [f"{idx}" for idx in range(i, i_end)]
    # add all to upsert list
    to_upsert = list(zip(ids, emb, meta))
    # upsert/insert these records to pinecone
    _ = index.upsert(vectors=to_upsert)

# check that we have all vectors in index
index.describe_index_stats()


def search_gif(query):
   # Generate embeddings for the query
   xq = retriever.encode(query).tolist()
   # Compute cosine similarity between query and embeddings vectors and return top 10 URls
   xc = index.query(xq, top_k=1,
                    include_metadata=True)
   result = []
   for context in xc['matches']:
      url = context['metadata']['responses']
      result.append(url)
   return result


def display_gif(urls):
   figures = []
   for url in urls:
      figures.append(f'''
            <figure style="margin: 5px !important;">
              <img src="{url}" style="width: 120px; height: 90px" >
            </figure>
        ''')
   return HTML(data=f'''
        <div style="display: flex; flex-flow: row wrap; text-align: center;">
        {''.join(figures)}
        </div>
    ''')

app = Flask(__name__)
app = Flask(__name__,template_folder='Templates', static_folder='static')

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')

def home():
    return render_template('index.html')

@app.route('/', methods =["GET", "POST"])
def responsesdata():

     if request.method == "POST":
        query=request.form["query"]
        gifs = search_gif(query)
        output=display_gif(gifs)
     return  render_template('index.html',q=query,odata=output)




if __name__ == '__main__':
   app.run()
