In recent years, Twitch has evolved from a gaming platform into one of the largest live social spaces on the internet. Millions of viewers actively participate in real-time chatrooms, forming tight-knit communities around streamers. However, as these communities grow, concerns have emerged about toxic behavior, polarization, and the spread of extreme language norms within and between chat communities.

This project aims to analyze the structure and language of Twitch chat communities to understand how streamers are connected through shared audiences and how linguistic tone and toxicity propagate across these networks. By combining network analysis and natural language processing, we will explore whether channels that share large portions of chatters also share similar language styles, emote cultures, or toxicity levels, and whether influential “hub” streamers act as bridges for spreading language norms across the platform.

Specifically, we will:
	1.	Construct a network of streamers based on shared active chatters.
	2.	Characterize each community’s language, sentiment, and toxicity using NLP models.
	3.	Investigate whether community structure correlates with differences in tone or extremity of language.

Ultimately, this project seeks to shed light on how online crowd behavior and linguistic polarization manifest in live digital spaces and whether platform network structure can help explain the rise of extreme or toxic subcultures within Twitch chat communities.

Project Structure:
├── notebooks/                              # Ordered exploratory analysis notebooks
│   ├── 00_network_construction.ipynb       # Data prep and graph building
│   ├── 01_basic_network_analysis.ipynb     # Degree, density, clustering
│   ├── 02_advanced_measures.ipynb          # Centrality and structural roles
│   ├── 03_network_clustering.ipynb         # Community detection experiments
│   ├── 04_text_processing.ipynb            # Cleaning and tokenizing chat logs
│   ├── 05_tfidf.ipynb                      # TF-IDF feature engineering
│   └── 06_sentiment_analysis.ipynb         # Sentiment & toxicity scoring
├── Proj3/                                  # Processed Twitch mention network artifacts
├── .gitignore
└── README.md                               # Project README
