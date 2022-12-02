# Documentation

## Links

### Packages used

- [googleapis/python-bigquery-pandas: Google BigQuery connector for pandas](https://github.com/googleapis/python-bigquery-pandas)
- [Mimino666/langdetect: Port of Google's language-detection library to Python.](https://github.com/Mimino666/langdetect)
- [nalepae/pandarallel: A simple and efficient tool to parallelize Pandas operations on all available CPUs](https://github.com/nalepae/pandarallel/)

### Source

- [minimaxir/gpt3-blog-title-optimizer: Python code for building a GPT-3 based technical blog post optimizer.](https://github.com/minimaxir/gpt3-blog-title-optimizer)
- [harrisonjansma/Medium_Scraper: The Selenium scraper that collected a million stories from Medium.com](https://github.com/harrisonjansma/Medium_Scraper)

### Scraping

- [testdrivenio/concurrent-web-scraping: Building a Concurrent Web Scraper with Python and Selenium](https://github.com/testdrivenio/concurrent-web-scraping/)
- [java - Selenium webdriver: Modifying navigator.webdriver flag to prevent selenium detection - Stack Overflow](https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904)
- [Multi-threaded Web Scraping with Selenium | by Rendra Sukana | Dev Genius](https://blog.devgenius.io/multi-threaded-web-scraping-with-selenium-dbcfb0635e83)
- [What I Learned from Scraping 15k Data Science Articles on Medium](https://khuyentran1476.medium.com/what-i-learned-from-scraping-15k-data-science-articles-on-medium-98a5f252d0aa) (got more data here)

### google cloud

- [Create and manage service account keys  |  IAM Documentation  |  Google Cloud](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)

### Code Formatting

- [Raise the Bar of Code Quality in Python Projects | by Baris Sari | Level Up Coding](https://levelup.gitconnected.com/raise-the-bar-of-code-quality-in-python-projects-7c49743f004f)
- [How I start every new Python backend API project](https://blog.szymonmiks.pl/p/how-i-start-every-new-python-backend-api-project/)

### OPEN AI

- [OpenAI family of models](https://beta.openai.com/docs/models/overview)
- [Pricing](https://openai.com/api/pricing/)
- [Fine-tuning](https://beta.openai.com/docs/guides/fine-tuning)
- [Fine-tuned classification example](https://github.com/openai/openai-cookbook/blob/main/examples/Fine-tuned_classification.ipynb)
- [Create fine-tune API docs](https://beta.openai.com/docs/api-reference/fine-tunes/create)
- [Completion create API docs](https://beta.openai.com/docs/api-reference/completions/create)
- [file upload API docs](https://beta.openai.com/docs/api-reference/files/upload)
- [What is sampling temperature?](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277)

### weights and biases

- [Fine-Tuning Tips and Exploration on OpenAI's GPT-3 – Weights & Biases](https://wandb.ai/borisd13/GPT-3/reports/GPT-3-exploration-fine-tuning-tips--VmlldzoxNDYwODA2) [(notebook)](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/openai/Fine_tune_GPT_3_with_Weights_%26_Biases.ipynb)
- [Fine-tune OpenAI GPT-3 on your own data and track results with W&B](https://docs.wandb.ai/guides/integrations/other/openai)

## Directory Structure

```txt
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── setup.py
├── data
│   ├── 0_external
│   ├── 0_raw
│   ├── 1_interim
│   └── 2_final
├── docs
│   └── README.md
├── notebooks
│   ├── 01_eda_cleaning.ipynb
│   ├── 02_GPT3_finetune_wb.ipynb
│   ├── 02_GPT3_metrics.ipynb
│   ├── 03_GPT3_log_inference.ipynb
│   └── 03_GPT3_prompting.ipynb
├── reports
│   └── figures
├── src
│   ├── __init__.py
│   ├── app
│   │   ├── Dockerfile
│   │   └── main.py
│   ├── data
│   │   ├── scraper.py
│   │   └── scraper_utils.py
│   ├── features
│   │   └── build_features.py
│   ├── models
│   │   ├── title_optimizer.py
└── tox.ini

```
