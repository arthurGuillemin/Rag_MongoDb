# rag-mongo

 RAG en utilisant MongoDB et AzureOpenAI.

## Configuration de l'environnement

Vous devez exporter deux variables d'environnement, l'une étant votre URI MongoDB, l'autre étant votre CLÉ API OpenAI.
Si vous n'avez pas d'URI MongoDB, consultez la section « Configurer Mongo » en bas pour obtenir des instructions sur la façon de procéder.

```shell
export MONGO_URI=...
export OPENAI_API_KEY=...
```

## Utilisation

Pour utiliser ce package, vous devez d'abord avoir installé la CLI LangChain :

```shell
pip install -U langchain-cli
```

Pour créer un nouveau projet LangChain et l'installer comme seul package, vous pouvez faire :

```shell
langchain app new my-app --package rag-mongo
```

Si vous souhaitez ajouter ceci à un projet existant, vous pouvez simplement exécuter :

```shell
langchain app add rag-mongo
```

Et ajoutez le code suivant à votre fichier `server.py` :
```python
from rag_mongo import chain as rag_mongo_chain

add_routes(app, rag_mongo_chain, path="/rag-mongo")
```

Si vous souhaitez configurer un pipeline d'ingestion, vous pouvez ajoutez le code suivant à votre fichier `server.py` :
```python
from rag_mongo import ingest as rag_mongo_ingest

add_routes(app, rag_mongo_ingest, path="/rag-mongo-ingest")
```


Si vous n'avez PAS déjà un index de recherche Mongo auquel vous souhaitez vous connecter, consultez la section `Configuration de MongoDB` ci-dessous avant de continuer.

Si vous avez un index de recherche MongoDB auquel vous souhaitez vous connecter, modifiez les détails de la connexion dans `rag_mongo/chain.py`

Si vous êtes dans ce répertoire, vous pouvez lancer directement une instance LangServe en :

```shell
langchain serve
```

Cela démarrera l'application FastAPI avec un serveur exécuté localement à
[http://localhost:8000](http://localhost:8000)

 pouvez voir tous les modèles à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
vous pouvez accéder au terrain de jeu à [http://127.0.0.1:8000/rag-mongo/playground](http://127.0.0.1:8000/rag-mongo/playground)

vous pouvez accéder au modèle à partir du code avec :

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-mongo")
```

Pour plus de contexte, veuillez vous référer à [ce bloc-notes](https://colab.research.google.com/drive/1cr2HBAHyBmwKUerJq2if0JaNhy-hIq7I#scrollTo=TZp7_CBfxTOB).

## Configuration de MongoDB

Utilisez cette étape si vous devez configurer MongoDB .


1. Créez un compte (si ce n'est pas déjà fait)
2. Créez un nouveau projet (si ce n'est pas déjà fait)
3. Récupérez votre URI MongoDB.

Définissons ensuite cela comme variable d'environnement localement :

```shell
export MONGO_URI=...
```

4. Définissons également une variable d'environnement pour AzureOpenAI (que vous utiliserons comme LLM)

```shell
export AZURE_OPENAI_API_KEY=...
```

5. Ingérons maintenant quelques données ! vous pouvez le faire en accédant à ce répertoire et en exécutant le code dans `ingest.py`, par exemple :

```shell
python ingest.py
```


6. vous devez maintenant configurer un index vectoriel sur nos données.

vous devez d'abord vous connecter au cluster où se trouve notre base de données 
ensuite naviguer jusqu'à l'endroit où toutes nos collections sont répertoriées
 puis ,  trouver la collection que vous voulons et consulter les index de recherche pour cette collection

Cela devrait normalement être vide, et vous voulons en créer un nouveau :


nous utiliserons le Éditeur JSON pour le créer 

Et collez le JSON suivant dans :

```text
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```


À partir de là, cliquez sur "Suivant" puis sur "Créer un index de recherche". Cela prendra un peu de temps, mais vous devriez alors avoir un index sur vos données !