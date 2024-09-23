# AppliRec: User-Based Collaborative Filtering for Appliances
In the ever-evolving landscape of e-commerce, customer reviews are pivotal in guiding purchasing decisions. Home appliances constitute a significant domain among the multitude of products available on platforms like Amazon. 
It is anticipated that the household appliances eCommerce market in the United States will reach US$48,404.9 million by the end of 2023, making up 84.3% of the country's electrical appliance eCommerce industry. 
Due to the fierce competition in the e-commerce market, it is important to harness new tools and technologies to be a market leader in a category. 
Analyzing and making use of the wealth of user-generated reviews in the Appliances category on Amazon can provide valuable insights into product preference and user sentiments. 
<br> <br>
The "AppliRec" project is designed to explore and leverage this vast repository of product reviews in the Appliances domain on Amazon. This project uses a user-based collaborative filtering recommendation system. 
E-commerce platforms witness significant demand for appliances like Cooktops, Ranges, Compactors, Trash Compactors, Dishwashers, Ice Makers, and Freezers, where the provided information plays a crucial role in purchasing decisions. Implementing a user-based recommendation system in such categories holds immense value. By showcasing products highly rated by users similar to an individual, this system becomes a pivotal tool. Its application across diverse sections of an e-commerce platform can enhance user engagement, prolong user sessions, and potentially increase the likelihood of successful checkouts.

### Links
<html>
  <body>
    <p>Project Report: <a href="https://drive.google.com/file/d/1hnlTe1xLmktABrRGf4yr6zjnuugxZrsn/view?usp=sharing">Click here to view the Project Report</a></p>
    <html>
    <p>Project Pitchdeck: <a href="https://drive.google.com/file/d/1Gl1LtujL7kBqJDiyk3Yq0mfmSKuylApZ/view?usp=sharing">Click here to view the Project Pitchdeck</a></p>
    </body>
</html>
    
### Contributors
Roshni Balasubramanian & Dhruv Arora <br>
In fulfilment of Modern Analytics (DECISION546Q), Duke University, Fuqua School of Business

## Deployment Instructions

This continuation of the work was done by Dhruv Arora as a personal project.
To replicate and deploy this project, follow the steps below:

#### 1. **Download the Data**
Run the following commands to download the necessary datasets:
```bash
wget https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/metaFiles2/meta_Appliances.json.gz
wget https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/categoryFiles/Appliances.json.gz
```
These data files will be excluded from version control due to the `.gitignore` settings.

#### 2. **Preprocess the Data**
Run the `preprocessing.py` script to preprocess the data and generate the intermediary file `preprocessed_data.csv`:
```bash
python preprocessing.py
```
This file will not be committed due to `.gitignore`.

#### 3. **Train the Model**
Next, train the recommendation model by running the `model.py` script. This will generate the trained model file `model_cf.pt`:
```bash
python model.py
```
The model file will also be excluded from the repository due to `.gitignore`.

#### 4. **Run the Flask Application Locally**
Start the Flask server by running `app.py`. The server will be hosted locally on port `5001`:
```bash
python app.py
```
You can then test the service by accessing `http://localhost:5001` using Postman or any HTTP client.

### Docker Deployment

#### 1. **Docker Image Setup**
To containerize the application, a `Dockerfile` is used with Gunicorn as the application server. The Docker image is built with the following commands:
```bash
docker build -t your-dockerhub-username/recommendation-system:v1 .
docker push your-dockerhub-username/recommendation-system:v1
```

#### 2. **Run Docker Container**
You can run the Docker container locally with:
```bash
docker run -p 5001:5001 your-dockerhub-username/recommendation-system:v1
```

### Gunicorn Setup

We use Gunicorn as the WSGI server to make the Flask app production-ready. Gunicorn handles concurrent requests efficiently.

```Dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

This is set in the Dockerfile to ensure the app runs on Gunicorn inside the container. This is already done but I have still added it here for context.

### Kubernetes & GCP Deployment

The application is deployed on **Google Kubernetes Engine (GKE)** for scalability and cloud deployment. The deployment steps involve creating a Kubernetes cluster, deploying the Docker container, and setting up a `LoadBalancer` service.

#### 1. **Set Up Kubernetes Cluster**
```bash
gcloud container clusters create recommendation-cluster --zone us-central1-a
gcloud container clusters get-credentials recommendation-cluster --zone us-central1-a
```

#### 2. **Deploy the Application on Kubernetes**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

#### 3. **Access the Application**
The application is exposed via a `LoadBalancer` service. Once deployed, you can access the application using the external IP provided by Kubernetes. Here is the external IP for the deployed service:

**External IP**: `34.45.205.66`

You can send requests to the `/predict` endpoint using Postman or curl.
