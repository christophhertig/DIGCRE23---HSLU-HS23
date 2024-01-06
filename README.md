# DIGCRE23 - Digital Creativity - Winter 2023

In this repository, I present my project for the Digital Creativity module in the Winter semester of 2023. The aim was to develop a project in the field of Artificial Intelligence that incorporates a creative aspect.

My concept involved analyzing the content from two news websites over several days. All articles from each website would be aggregated daily, and from this extensive text, 10 keywords would be extracted. The outcome should be 10 words per day per website. Using these words, images would be generated using generative AI. The images should reflect the mood or significant events of the day.

## 1. Web Scraping
For the experiment, the websites [srf.ch](https://www.srf.ch/) and [blick.ch](https://www.blick.ch/) were utilized. To fetch the current articles, the RSS feed of both websites was employed. From the RSS feed, the links to the articles were extracted, and subsequently, the contents of the articles were downloaded. For this task, Python libraries such as BeautifulSoup, Feedparser, and Requests were utilized. The contents of the websites were extracted using the Python libraries BeautifulSoup, Feedparser, and Requests.

### Notebook [WebScraping_experiment](WebScraping_experiment.ipynb)
The notebook [WebScraping_experiment](WebScraping_experiment.ipynb) documents the code and process for web scraping. It aims to help understand the process. Within the notebook, the contents of the websites are extracted, structured, stored in DataFrames, and then saved as CSV files. Subsequently, a script was developed using the insights from the notebook to automatically download the contents of the websites.


### Script [main.py](main.py)
The contents of the notebook [WebScraping_experiment](WebScraping_experiment.ipynb) have been transferred to a script. The script downloads the contents of the websites and saves them in CSV files. The structure of the .CSV file is as follows:


Example:

| title                                      | link                                           | published                    | published_parsed                  | article_content                                                                                      |
|--------------------------------------------|------------------------------------------------|------------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------|
| Winner of the Grand Prix Literature: Author Ann... | https://www.blick.ch/news/winner-of-the-grand-... | Thu, 16 Nov 2023 13:54:05 GMT | (2023, 11, 16, 13, 54, 5, 3, 320, 0) | When writing, Anna Felder is always very...

The goal is to save the articles daily over several days. To obtain consistent results, it's crucial to execute the script at the same time each day. To avoid turning on the laptop at the same time every day, the script was deployed on a Raspberry Pi. The Raspberry Pi is configured to run the script daily at 23:45.  

The file name is structured as follows:

```
    day_month_year_hour_website.csv
```

The following sources were used for web scraping:
- [How to install pip on the Raspberry Pi](https://pimylifeup.com/raspberry-pi-pip/)
- [Python Job Scheduling with Cron](https://www.advsyscon.com/blog/python-job-scheduling/)
- [Transfer files and folders from Windows to Linux with PSCP](https://opensource.com/article/22/10/transfer-files-windows-linux-pscp)

## 2. Keyword Extraction
Various approaches were attempted for keyword extraction. Many Natural Language Processing (NLP) models are trained in English and do not function in German. Since the articles are in German, the initial approach was to translate all articles from German to English. However, this approach proved to be ineffective. The volume of data was underestimated. For each website and day, up to 60 articles were aggregated, with an article containing approximately 3,000 characters. When combined, this resulted in a maximum of 180,000 characters for a single day of one website, which was too long for the NLP translation models to handle. Moreover, this would have been computationally intensive.

After further experimentation, a new approach was adopted. The idea of concatenating the article texts was abandoned as the resulting text corpus was too large. It was decided to only concatenate the article titles. Titles are concise and contain the most crucial information. Additionally, titles do not contain many stop words like "der, die, ein, an, in," simplifying the data preprocessing. Thus, a text corpus of around 3,000 characters was generated for each website and day.

### Notebook [keyBERT.ipynb](keyBERT.ipynb)
After further research, the idea of translation was discarded. A model was found that works with German texts, using [KeyBERT](https://maartengr.github.io/KeyBERT/). To process the German texts, the Sentence Transformers model [distiluse-base-multilingual-cased-v1](https://www.sbert.net/docs/pretrained_models.html) was chosen. The implementation is documented in the notebook [keyBERT.ipynb](keyBERT.ipynb).  

The output has the following structure:
| file  | keywords_combined |
|-------|-------------------|
| 23_11_18_23_blick.csv | "['schweiz', 'gefahr', 'unfall', 'feuer', 'ukrainischen', 'russische', 'schockierende', 'verschreckte', 'jordan', 'jugendliche']" |
| 23_11_18_23_srf.csv | "['politik', 'wofür', 'thailand', 'energieversorger', 'wiederwahl', 'bern', 'sprintrennen', 'niederlande', 'vermieter', 'schweiz']" |

## Experiment: Saturday, 18th Nov to Friday, 24th Nov 2023
For the experiment, articles from both websites were downloaded from Saturday, 18th Nov to Friday, 24th Nov 2023. The downloaded articles are stored in the folder data/articles/. The extracted keywords are saved in the .CSV file [articles_title_keywords_23_11_18-23.csv](/data/articles_title_keywords_23_11_18-23.csv). An initial analysis of the keywords was conducted using [ydata-profiling](https://docs.profiling.ydata.ai/latest/), generating an HTML report.

The following image displays the most frequent keywords from both websites during the week from 18th Nov to 24th Nov 2023.

<img src="images/wordcloud.png" alt="Word Cloud" width="500">

## Generating Images
Images were generated using keywords. For this purpose, the service from [Bing Image Creator AI](https://www.bing.com/images/create) was utilized.

### 1. Attempt: Keywords with a Specific Style
The keywords from 21.11.2023 from the website were utilized.  
Keywords: snow, traffic accident, minivan, North Korea, shot, billion fine, black, Bern, foreigner.  
Using these words and the style "Digital Cubism," the following image was generated:

![21_11_21_21_blick_digitalcubism](images/23_11_21_23_blick_digitalcubism.jpg)

The result is not very satisfactory. The images lack clarity. While elements of the keywords can be identified, such as snow, traffic accident, and the city resembling Bern with its distinctive church and snow-capped mountains in the background (Bernese and Valais Alps).

### 2. Attempt: ChatGPT Story
After further research, a new approach was adopted. A story was to be generated using the keywords. For this, the keywords were used to generate a one-sentence story in English using ChatGPT. This story was then passed to Bing Image Creator AI.  
The same keywords as in the first attempt (21.11.2023, Blick.ch): snow, traffic accident, minivan, North Korea, shot, billion fine, black, Bern, foreigner.  
Story generated by ChatGPT: A Swiss minivan driver from Bern, traveling in the snow, got into a traffic accident and had to pay a hefty fine after accidentally crossing into North Korea and colliding with a foreigner dressed in black.

The following images were generated using Bing Image Creator AI:

| ![Image 1](images/23_11_21_23_blick_story_v1.jpg) | ![Image 2](images/23_11_21_23_blick_story_v2.jpg) | ![Image 3](images/23_11_21_23_blick_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|

In my opinion, the results with this approach were better. The images are more meaningful and contain various elements of the keywords.

The experiment was conducted with the keywords from the same day (21.11.2023) using the SRF website.  
Keywords: recycling, Rapperswil, Federal Palace, Orban, positioned, protest ban, Swiss, Switzerland, finance ministry, federal budget.  
ChatGPT Story: In Rapperswil, Switzerland, the Finance Ministry takes a stance against a protest ban outside the Federal Palace and emphasizes the importance of recycling in the federal budget, despite Orban's position.

| ![Image 1](images/23_11_21_23_srf_story_v1.jpg) | ![Image 2](images/23_11_21_23_srf_story_v2.jpg) | ![Image 3](images/23_11_21_23_srf_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|------------------------------------------------|

### Another Attempt, Same Day for blick.ch and srf.ch: 19.11.2023
Keywords from 19.11.2023, Blick.ch: flowers, mobilization, crash, golf balls, wolf hunt, depth, Argentine, Israeli, Senate elections, Federal Council candidates  
Story: In a deep mobilization ahead of the Senate elections, flowers and golf balls were used in protest against the Israeli wolf hunt, while an Argentine criticizes federal council candidates.

| ![Image 1](images/23_11_19_23_blick_story_v1.jpg) | ![Image 2](images/23_11_19_23_blick_story_v2.jpg) | ![Image 3](images/23_11_19_23_blick_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|


Keywords from 19.11.2023, srf.ch: election winner, candidate, left, leftist, Swiss, Schaffhausen, antisemitism, Djokovic, volcano risk, Hersberg  
Story: After becoming the victorious candidate in Schaffhausen, a Swiss left-wing politician faces controversy over alleged anti-Semitism, while simultaneously warning of potential volcanic threats akin to Djokovic's unpredictability in Hersberg.

| ![Image 1](images/23_11_19_23_srf_story_v1.jpg) | ![Image 2](images/23_11_19_23_srf_story_v2.jpg) | ![Image 3](images/23_11_19_23_srf_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|


### Another Attempt, Same Day for blick.ch and srf.ch: 18.11.2023
Keywords from 19.11.2023, Blick.ch: Switzerland, danger, accident, fire, Ukrainian, Russian, shocking, startled, Jordan, youths  
Story: In Switzerland, residents witnessed an unexpected incident where Ukrainian and Russian youths had a surprising encounter, causing concern and excitement, especially for Jordan.

| ![Image 1](images/23_11_18_23_blick_story_v1.jpg) | ![Image 2](images/23_11_18_23_blick_story_v2.jpg) | ![Image 3](images/23_11_18_23_blick_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|

Keywords from 19.11.2023, srf.ch: politics, for what, Thailand, energy provider, re-election, Bern, sprint race, Netherlands, landlord, Switzerland  
Story: In politics, a Thai energy provider's bid for re-election in Bern mirrors the unpredictability of sprint races in the Netherlands, while Swiss landlords grapple with new regulations at home.

| ![Image 1](images/23_11_18_23_srf_story_v1.jpg) | ![Image 2](images/23_11_18_23_srf_story_v2.jpg) |
|--------------------------------------------------|--------------------------------------------------|

### Conclusion: Website Comparison
The images from the two websites differ significantly. Due to different keywords, entirely different images were produced. Comparing the images was intriguing. However, it's not entirely conclusive since the keyword extraction model wasn't perfectly implemented.


## Closing Thoughts
The project provided many exciting insights. It was my first time working with web scraping and Raspberry Pi, allowing me to learn a lot of new things. I was especially able to gather good methods and experiences for future projects. The resource-efficient Raspberry Pi has many potential applications. It was particularly exciting to implement one's creativity and ideas without significant constraints.






<!-- 
# DIGCRE23 - Digital Creativity - Winter 2023
 
 Ich folgendem Repository präsentiere ich mein Projekt für das Modul Digital Creativity im Wintersemester 2023.Das Ziel war es, im Feld von Künstlicher Intellegenz ein Projekt zu entwickeln, welches einen kreativen Aspekt beinhaltet.  

 Meine Idee war es, über einige Tage die Inhalte von zwei News-Websites zu analysieren. Alle Artikel der Website sollen pro Tag zusammengeführt werden und von diesem grossen Text sollen 10 Keywords extrahiert werden. Das Ergebnis sollten somit 10 Wörter pro Tag und pro Website sein. Mittels diesen Wörtern werden dann Bilder mittels generative ai Bilder generiert. Die Bilder sollen die Stimmung oder wichtige Ergeignisse des Tages wiederspiegeln.  

## 1. Web scraping
 Für das Experiment wurden die Websites von [srf.ch](https://www.srf.ch/) und [blick.ch](https://www.blick.ch/) verwendet. Um die aktuellen Artikel abzurufen wurde der RSS-Feed der beiden Websites verwendet. Vom RSS-Feed wurden die Links zu den Artikeln extrahiert und anschliessend die Inhalte der Artikel heruntergeladen. Hierfür wurden die Python Libraries BeautifulSoup, Feedparser und Requests verwendet. Mithilfe der Python Library BeautifulSoup, Feedparser und Requests wurden die Inhalte der Websites extrahiert.  
 
 ### Notebook [WebScraping_experiment](WebScraping_experiment.ipynb)
 Im Notebook [WebScraping_experiment](WebScraping_experiment.ipynb) ist der Code und Vorgang für das Web Scraping dokumentiert. Das Notebook soll helfen, den Vorgang nachzuvollziehen. Im Notebook werden die Inhalte der Websites extrahiert, strukturiert, in DataFrames abgelegt und anschliessend in CSV-Dateien gespeichert. Mithilfe des Notebooks wurde anschliessend ein Script erstellt, welches die Inhalte der Websites automatisch herunterlädt. 

 ### Script [main.py](main.py)
 Die Inhalte des Notebooks [WebScraping_experiment](WebScraping_experiment.ipynb) wurden in ein Script übertragen. Das Script lädt die Inhalte der Websites herunter und speichert diese in CSV-Dateien. Die Struktur des .CSV Files ist wie folgt:

  ```
    title, link, published, published_parsed, article_content
 ```

 Beispiel:

| title                                      | link                                           | published                    | published_parsed                  | article_content                                                                                      |
|--------------------------------------------|------------------------------------------------|------------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------|
| Trägerin des Grand Prix Literatur: Autorin Ann... | https://www.blick.ch/news/traegerin-des-grand-... | Thu, 16 Nov 2023 13:54:05 GMT | (2023, 11, 16, 13, 54, 5, 3, 320, 0) | Beim Schreiben ist Anna Felder stets sehr bedä...

Das Ziel ist es, über mehrere Tage jeweils tageweise die Artikel zu speichern. Um konsistente Ergebnisse zu erhalten ist es wichtig, dass das Skript immer zur gleichen Zeit ausgeführt wird. Damit der Laptop nicht immer zur gleichen Zeit eingeschaltet werden muss, wurde das Skript auf einem Raspberry Pi hinterlegt. Der Raspberry Pi ist so konfiguriert, dass er mittels Cronjob das Skript täglich um 23:45 Uhr ausführt.


Mithilfe folgender Quellen wurde das Web Scraping realisiert:
- [How to install pip on the Raspberry Pi](https://pimylifeup.com/raspberry-pi-pip/)
- [Python Job Scheduling with Cron](https://www.advsyscon.com/blog/python-job-scheduling/)
- [Transfer files and folders from Windows to Linux with PSCP](https://opensource.com/article/22/10/transfer-files-windows-linux-pscp)

## 2. Keyword Extraction
Für das Keyword Extraction wurden verschiedene Ansätze versucht. Viele Natural Language Processing (NLP) Modelle sind auf Englisch trainiert und funktionieren nicht auf Deutsch. Da die Artikel in Deutsch sind, war der erste Ansatz, alle Artikel von Deutsch ins Englische zu übersetzen. Dieser Ansatz hat sich als nicht zielführend erwiesen. Die Menge an Daten wurde unterschätzt. Pro Website und pro Tag kamen bis zu 60 Artikel zusammen, wobei ein Artikel rund 3'000 Zeichen aufweist. Alle Artikel zusammengeführt ergab somit im Maximum 180'000 Zeichen für einen einzelnen Tag einer Website. Diese Länge war für die Untersuchten NLP Translationsmodelle zu lang. Die Modelle konnten die Texte nicht übersetzen. Zudem wäre dies auch sehr rechenintensiv gewesen.  

Nach weiterer Experimenten wurde ein neuer Ansatz gewählt. Es wurde von der Idee abgewichen, die Artikel-Texte zusammenzufügen. Offensichtlich ist der so erhaltene Textkorpus schlicht zu gross. Es wurde entschieden, dass lediglich die Titel der Artikel zusammengeführt werden. Die Titel sind kurz und enthalten die wichtigsten Informationen. Weiter sollten in den Titeln auch nicht viele Stoppwörter wie z.B. "der, die, ein, an, in" vor kommen, dies vereinfacht die Vorverarbeitung der Daten. Somit entstand pro Website und pro Tag ein Textkorpus von rund 3'000 Zeichen.  


### Notebook [keyBERT.ipynb](keyBERT.ipynb)
Nach weiterer Recherche wurde die Idee mit dme Übersetzen verworfen. Es wurde ein Modell gefunden, welches mit Deutschen Texten funktioniert. Herfür wurde [KeyBERT](https://maartengr.github.io/KeyBERT/) verwendet. Damit die deutschen Texte verarbeitet werden können, wurde als Sentence Transformers Modell [distiluse-base-multilingual-cased-v1](https://www.sbert.net/docs/pretrained_models.html) gewählt. Die Umsetzung ist im Notebook [keyBERT.ipynb](keyBERT.ipynb) dokumentiert.

## Experiment: Samstag, 18.11. bis Freitag, 24.11.2023
Für das Experiment wurden die Artikel der beiden Websites von Samstag, 18.11. bis Freitag, 24.11.2023 heruntergeladen. Die heruntergeladenen Artikel sind im Ordner data/articles/ abgelegt. Die extrahierten Keywords sind im .CSV File [articles_title_keywords_23_11_18-23.csv](/data/articles_title_keywords_23_11_18-23.csv) abgelegt. Eine erste Analyse der Keywords wurde mithilfe von [ydata-profiling](https://docs.profiling.ydata.ai/latest/) durchgeführt. Hiermit wurde ein HTML Report generiert.  

Das nachfolgende Bild zeigt die häufigsten Keywords der beiden Websites während der Woche vom 18.11. bis 24.11.2023.

<img src="images/wordcloud.png" alt="Word Cloud" width="500">


## Bilder generieren
Mithilfe der Keywords wurden Bilder generiert. Hierfür wurde der Dienst von [Bing Image Creator AI](https://www.bing.com/images/create).

### 1. Versuch: Keywords mit einem bestimmten Stil
Es wurden die Keywords vom 21.11.2023 von der Website verwendet.  
Keywords: schnee, verkehrsunfall, minivan, nordkorea, erschossen, milliardenstrafe, black, bern, ausländer.  
Mit diesen Worten und dem Stil "Digial Cubism" wurde nachfolgendes Bild generiert:

![21_11_21_21_blick_digitalcubism](images/23_11_21_23_blick_digitalcubism.jpg)

Das Resultat ist nicht sehr zufriedenstellend. Die Bilder sind nicht sehr aussagekräftig. Es sind zwar Elemente der Keywords zu erkennen, wie zum Beispiel Schnee, Verkehrsunfall und die Stadt erinnert mit der markanten Kirche und den schneebedeckten Bergen im Hintergrund (Berner und Walliser Alpen) an Bern.

### 2. Versuch: ChatGPT Story
Nach weiterer Recherche wurde ein neuer Ansatz gewählt. Mit den Keywords soll eine Geschichte generiert werden. Hierfür wurden die Keywords genommen und mittels ChatGPT eine 1-Satz-Story auf englisch generiert werden. Die Story wurde anschliessend an Bing Image Creator AI übergeben.  
Dieselben Keywords wie im ersten Versuch (21.11.2023, Blick.ch): schnee, verkehrsunfall, minivan, nordkorea, erschossen, milliardenstrafe, black, bern, ausländer.  
Durch ChatGPT erzeugte Story: A Swiss minivan driver from Bern, traveling in the snow, got into a traffic accident and had to pay a hefty fine after accidentally crossing into North Korea and colliding with a foreigner dressed in black.


Folgende Bilder wurden mit Bing Image Creator AI generiert:

| ![Bild 1](images/23_11_21_23_blick_story_v1.jpg) | ![Bild 2](images/23_11_21_23_blick_story_v2.jpg) | ![Bild 3](images/23_11_21_23_blick_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|

Die Resultate mit diesem Ansatz waren meiner Meinung nach besser. Die Bilder sind aussagekräftiger und enthalten diverse Elemente der Keywords.  

Das Experiment wurde mit den Keywords desselben Tages (21.11.2023) mit der Website von SRF durchgeführt.  
Keywords: recycling, rapperswil, bundeshaus, orban, positioniert, demoverbot, schweizer, schweiz, finanzministerium, bundeshaushalt  
ChatGPT Story: In Rapperswil, Switzerland, the Finance Ministry takes a stance against a protest ban outside the Federal Palace and emphasizes the importance of recycling in the federal budget, despite Orban's position.  

| ![Bild 1](images/23_11_21_23_srf_story_v1.jpg) | ![Bild 2](images/23_11_21_23_srf_story_v2.jpg) | ![Bild 3](images/23_11_21_23_srf_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|------------------------------------------------|

Auch hier sind einige Keywors in den Bildern zu erkennen, wie z.B. Bundeshaus, Demoverbot, Recycling, Schweiz.


### Weiterer Versuch, gleicher Tag blick.ch und srf.ch: 19.11.2023
Keywords vom 19.11.2023, Blick.ch: blumen, mobilisierung, crash, golfbälle, wolfsjagd, tiefe, argentinier, israelische, ständeratswahlen, bundesratskandidaten  
Story: In a deep mobilization ahead of the Senate elections, flowers and golf balls were used in protest against the Israeli wolf hunt, while an Argentine criticizes federal council candidates  

| ![Bild 1](images/23_11_19_23_blick_story_v1.jpg) | ![Bild 2](images/23_11_19_23_blick_story_v2.jpg) | ![Bild 3](images/23_11_19_23_blick_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|


Keywords vom 19.11.2023, srf.ch: wahlsiegerin, kandidat, linke, linkem, schweizer, schaffhausen, antisemitismus, djokovic, vulkangefahr, hersberg  
Story: After becoming the victorious candidate in Schaffhausen, a Swiss left-wing politician faces controversy over alleged anti-Semitism, while simultaneously warning of potential volcanic threats akin to Djokovic's unpredictability in Hersberg.

| ![Bild 1](images/23_11_19_23_srf_story_v1.jpg) | ![Bild 2](images/23_11_19_23_srf_story_v2.jpg) | ![Bild 3](images/23_11_19_23_srf_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|


### Weiterer Versuch, gleicher Tag blick.ch und srf.ch: 18.11.2023
Keywords vom 19.11.2023, Blick.ch: schweiz, gefahr, unfall, feuer, ukrainischen, russische, schockierende, verschreckte, jordan, jugendliche  
Story: In Switzerland, residents witnessed an unexpected incident where Ukrainian and Russian youths had a surprising encounter, causing concern and excitement, especially for Jordan.

| ![Bild 1](images/23_11_18_23_blick_story_v1.jpg) | ![Bild 2](images/23_11_18_23_blick_story_v2.jpg) | ![Bild 3](images/23_11_18_23_blick_story_v3.jpg) |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|

Keywords vom 19.11.2023, srf.ch: politik, wofür, thailand, energieversorger, wiederwahl, bern, sprintrennen, niederlande, vermieter, schweiz
Story: In politics, a Thai energy provider's bid for re-election in Bern mirrors the unpredictability of sprint races in the Netherlands, while Swiss landlords grapple with new regulations at home.

| ![Bild 1](images/23_11_18_23_srf_story_v1.jpg) | ![Bild 2](images/23_11_18_23_srf_story_v2.jpg) |
|--------------------------------------------------|--------------------------------------------------|

### Fazit Website Vergleich
Die Bilder von den zwei Websites unterscheiden sich stark. Aufgrund anderer Keywords ergaben sich völlig andere Bilder. Es war spannend, die Bilder zu vergleichen. Ganz aussagekräftig ist es jedoch nicht, da das Keyword Extraction Modell nicht perfekt umgesetzt wurde.


## Schlusswort
Das Projekt gab sehr viele spannende Erkenntnisse. Mit dem Web scraping und Raspberry Pi habe ich das erste Mal gearbeitet. Somit konnte ich sehr viel neues lernen. Vor allem auch gute Methoden und Erfahrungen für zukünftige Projekte sammeln. Mit dem Ressourcenschonenden Raspberry Pi gibt es noch viele gute Einsatzbereiche. Es war vor allem auch spannend, die eigene Kreavitität und Ideen ohne grosse Einschränkungen umzusetzen. -->


