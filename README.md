# Smart-Giffy
Gif Based chatbot replies in gif according to user query

## Data Base
  Pinecone
## Model
  * Sentence transformer
  #### Short Description:
  This model is used for text and Image Embeddings
## Web Framwork
   * Flask
  
# Steps to follow:
1) Install the libraries
  * Pandas
  * Pinecone-client
  * Tqdm(progress bar)
2) Read the data in which is tsv(Tab seperated file) format
  ![image](https://user-images.githubusercontent.com/67852967/202750293-298e1796-a931-4db2-b2f0-960f0e5f64df.png)

3) Convert the tsv to csv.
4) connect to the database
   * Give the API key
   * Dimensions
   * Metrics ** cosine **
5) Download the model
   * sentence-transformers/all-MiniLM-L6-v2
6) Insert the data to database
   * Encode the text to vector
   * Create the id's for text 
   * Update the database
7) search the query 
   * Encode the text to vector
   * Find the text with the existed text in the database
   * Return the Gif
   
8) Display the gif
   ![image](https://user-images.githubusercontent.com/67852967/202752814-e0f36fc2-326c-42f5-a3ec-e02dec29f050.png)
 
9) Build the chatbot
   ![image](https://user-images.githubusercontent.com/67852967/202753294-763ef269-f014-4253-af6e-b37e5f2fb0ee.png)









