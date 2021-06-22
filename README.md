# SentOpin


## Description

Globalization is everywhere. Big companies have distributed branches, but how management can be sure that customer experience at high level in all locations?

We have decided to check opinions about different branches of insurance companies in the USA.

### Our POC suggests such flow:
	
1. Customer enters search string for locations and just wait for results 
2. Our background processing finds all related locations with reviews on Google maps. Then apply expert.ai NLP API Full and Classification analysis 
3. After that Status for current became "Finished" and the customer can check result on charts 

For the demo, we've gathered reviews from all available locations for few companies. After processing reviews thru expert.ai NLP API, we've noticed a few things.
	
1. Insurance agents have higher overall sentiment than, regular offices
2. Geographical distribution can differ from coast to coast
3. Some commercials made people angry, this can surprise marketing departments :)
4. Entities from expert.ai allow to catch comments, addressed personally
5. Classification from expert.ai allows finding cases, where customers addressing the area of problematic topic


**Using expert.ai API in our solution will empower business with data driven decision making abilities.**

## How to start application 

```
python manage.py runserver
```

## How to use 

1. Open: 

http://localhost:8000/admin/reviews/search/ 

2. Use credentials to log in:  

username: `demo`

password: `demo`


## Dev notes 

Apply migrations: 
```
python manage.py migrate 
```

Create user:
```
python manage.py createsuperuser
```

Create migrations: 
```
python manage.py makemigrations 
```



 python manage.py makemigrations reviews