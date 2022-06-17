# F1 Insights

## Context

Realized as the final project of the [Jedha Bootcamp FullStack course](https://en.jedha.co/formations/formation-data-scientist), and was completed in the first two weeks of June 2022. It is written almost entirely in Python.

The team is composed of:

* Adrien: [Linkedin](https://www.linkedin.com/in/adrienory) / [Github](https://github.com/AdrienOry)
* Bérenger: [Linkedin](https://www.linkedin.com/in/berenger-queune/) / [Github](https://github.com/BerengerQueune)
* Christophe: [Linkedin](https://www.linkedin.com/in/clefebvre78/) / [Github](https://github.com/clefebvre2021)
* Guillaume: [Linkedin](https://www.linkedin.com/in/guillaumearp/) / [Github](https://github.com/GuillaumeArp)

-----

## Content

The aim of this project is to provide a dashboard for Formula 1 fans and allow them to explore the racing data a bit further, with detailed telemetry visualizations, lap comparisons, and other insights regarding the current standings.

At this point, this will only work for the 2022 season. Implementation of forthcoming seasons may be added in the future, if there is an interest.

The dashboard is freely accessible online on [this page](http://f1insights-env.eba-kkbkzqy2.eu-west-3.elasticbeanstalk.com/). Please note that performance improvement is still our biggest challenge, and any user should be careful about changing sessions too fast. Please also wait until each page is fully loaded before clicking on anything else.

-----

## Tech Stack

### Data Sources and Storage

* [Fast F1 API](https://theoehrly.github.io/Fast-F1/index.html)
* [Ergast API](https://ergast.com/api/f1)
* [AWS S3](https://aws.amazon.com/s3/)

### Data Processing and Visualizations

* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)
* [Plotly](https://plotly.com/python/)

### Web App

* [Streamlit](https://streamlit.io/)

### Deployment

* [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
* [Heroku](https://www.heroku.com/)
