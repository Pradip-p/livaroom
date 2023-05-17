## Price Matching Tools

This project aims to scrape data from two websites, https://englishelm.com/ and https://livaroom.com/, and save the scraped data into a database for prices comparison and also can update the optimal price of product on livaroom.

#### Requirements
To run this project, you need to have the following software installed:

1. Python 3.x
2. Django
3. Scrapy 
4. Requests library
5. ShopifyAPI
6. Database management system (e.g.PostgreSQL)

#### Setup
1. Clone the repository or download the source code.
```
git clone git@github.com:Pradip-p/livaroom.git

```
2. Install the required dependencies.
```
pip install -r crawler/requirements.txt
```
#### Usage
1. Run the english.py script to scrape data from https://englishelm.com/ and save it to the database.
```
python crawler/english.py

```

2. Run the livaroom_com.py script to scrape data from https://livaroom.com/ and save it to the database.
```
python crawler/livaroom_com.py

```
3. After running both scripts, the scraped data will be stored in the database.

#### Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please submit a pull request.

#### License
This project is licensed under the MIT License.

