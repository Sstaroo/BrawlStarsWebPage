# DATABASE AND APPWEB PROJECT

## Brawl Stars project 

This project focuses on creating a database for the popular video game Brawl Stars. The database collects information from player rankings, clubs, and the use of different characters in the game (Brawlers). The main objective is to provide a structured schema to analyze the performance of different elements of the game over time and by region.

### Motivation

This project seeks to answer questions such as:

*   Who are the best players in the world?
*   What are the most used Brawlers by the best players?
*   How does the use of Brawlers vary by country and month?

The analysis of this data can be very useful for both casual players and those looking to reach the top of the world ranking.

### Data source

The data used in this project comes from the following Kaggle dataset:

*   https://www.kaggle.com/datasets/albertovidalrod/brawl-stars-rankings-players-and-clubs

**Reference:**

*   Vidal Rodríguez, A. (2023). Brawl Stars - Rankings, players and clubs [Dataset]. Kaggle.

### Data model

The project has gone through two versions of the data model: "pre-milestone3" and "post-milestone3". Although the official model is "post-milestone3", it has been decided to keep the information from the previous version to show the evolution of the project.

#### Version "pre-milestone3"

This version included the following entities:

*   Player
*   Club
*   Brawler
*   Country
*   Month

The Player and Club entities were limited to the top 200 representatives in each category. The Country and Month entities were used to organize players and clubs across space and time. The Brawler entity contemplated the top 200 players who use each character.

The relational model was based on the following tables:

*   Player (`tag\_j`, `np, name\_j`, `colorName`, `icon`, `trophies\_j`, `rank\_p`)
*   Club (`tag\_c`, `np`, `name\_c`, `numberOfMembers`, `totalTrophies`, `rank\_c`, `badgeId`, `rank\_p`)
*   Brawler (`name\_b`, `tagPlayer`, `np`, `rank\_b`, `trophies\_b`)
*   Country (`name\_p`, `trophies\_p`)
*   Month (`name\_m`)
*   Belongs (`j1`, `j2`, `c1`, `c2`)
*   Determines (`c\_p1`, `c\_p2`, `c\_p3`, `nm`)
*   Defines (`j\_p1`, `j\_p2`, `j\_p3`, `nm`)

The LeCorresponde, Representa, and LoPosee relations were implicitly represented through foreign keys.

#### Version "post-milestone3"

This version was restructured to improve data integrity and consistency. New entities and relationships were introduced to represent the dynamics of the game more accurately.

The new relational model includes the following tables:

*   Player (`player\_tag`, `player\_name`, `color\_name`, `icon`, `country\_name`)
*   Club (`club\_tag`, `club\_name`, `country\_name`)
*   Brawler (`brawler\_id`, `brawler\_name`)
*   Country (`country\_name`)
*   Month (`month\_name`, `year`)
*   PlaysWith (`relation\_id`, `player\_tag`, `brawler\_name`, `month\_name`, `trophies`, `position`)
*   Club\_Country\_Ranking (`ranking\_id`, `club\_tag`, `country\_name`, `month\_name`, `trophies`, `position`)
*   Club\_Evolution (`relation\_id`, `club\_tag`, `month\_name`, `total\_trophies`, `members`)
*   Player\_Country\_Ranking (`ranking\_id`, `player\_tag`, `country\_name`, `month\_name`, `total\_trophies`, `position`)
*   Trophies\_Country\_200\_Player (`relation\_id`, `country\_name`, `month\_name`, `total\_trophies`)
*   Trophies\_Country\_200\_Club (`relation\_id`, `country\_name`, `month\_name`, `total\_trophies`, `total\_members`)
*   Trophies\_200\_Brawler (`relation\_id`, `brawler\_name`, `month\_name`, `total\_trophies`)



Major changes were made to the relationships, the use of identifiers, and the introduction of summary tables by country.

### Implementation

The database was implemented on the cc3201.dcc.uchile.cl server using PostgreSQL. A schema called "ProyectBrawlStars" was created to house the tables.

The data was loaded into the tables using a Python script that processes the CSV files downloaded from Kaggle.

### Web application

A web application was developed to query the database and visualize the results. The application is hosted at the following URL:

*   https://grupo19.cc3201.dcc.uchile.cl/

The web application includes the following sections:

*   Main page (index.html)
*   Top Players (top\_players.php)
*   Top Clubs (top\_clubs.php)
*   Top Brawlers (top\_brawlers.php)
*   Interactive queries (consulta1.php, consulta2.php, consulta3.php, consulta4.php)

Interactive queries allow users to filter results by different parameters, such as month, country, or Brawler name.

### Security

Security measures were implemented to prevent SQL injections and other vulnerabilities in the web application. These measures include:

*   Use of prepared queries with PDO
*   Input validation
*   Output escaping with htmlspecialchars
*   Setting the error mode with PDO
*   Error handling with try-catch

### Preview and Visalization
You can check it out at https://youtu.be/J-L_O_B0i9Y?si=9eJY-6HnZbEskWy0 

### Conclusions

This project provides a robust database and web application to analyze Brawl Stars data. Analysis of this data can help players understand game trends, improve their performance, and learn from the best.
