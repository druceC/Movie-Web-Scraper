from bs4 import BeautifulSoup
import requests
import csv 

# Function to extract info box of movie 
def extract_movie_details(url):

	# Get web site content
	html = requests.get(url)

	# Parse html
	soup = BeautifulSoup(html.content, features='html.parser')

	info_box = soup.find('table',{'class':'infobox vevent'})
	rows = info_box.find_all('tr')

	# Empty dictionary created to store movie info
	movie_info = {}

	# Initialize relevant info
	movie_info["Release dates"]="."
	movie_info["Release date"]="."
	movie_info["Running time"]="."
	movie_info["Budget"]="."
	movie_info["Box office"]="."

	for index,row in enumerate(rows):
		if index == 0:
			movie_info["Title"]=row.find("th").getText()
		else:
			# Check rows for header tag
			header = row.find('th')
			if header:
				key = row.find('th').getText(" ")
				if row.find('td'):
					value = row.find('td').getText(" ").replace("\xa0","").replace("\n","")
				else:
					value = [item.getText() for item in row.find_all('li')]
				
				# Assign value variable as the corresponding dictionary value for the movie
				movie_info[key] = value

	return(movie_info)


# Function that gets the urls of each animated movie produced by a production

urls = ["https://en.wikipedia.org/wiki/List_of_Walt_Disney_Animation_Studios_films","https://en.wikipedia.org/wiki/List_of_Pixar_films","https://en.wikipedia.org/wiki/List_of_Illumination_productions","https://en.wikipedia.org/wiki/List_of_Sony_Pictures_Animation_productions","https://en.wikipedia.org/wiki/List_of_DreamWorks_Animation_productions"]
csv = ["disney.csv","pixar.csv","illumination.csv","sony.csv","dreamworks.csv"]

for x in range(5):
	get_movies(urls[x],csv[x])

def get_movies(url_,csvFile):
	movielist=[]
	html = requests.get(url_)

	soup = BeautifulSoup(html.content, features="lxml")
	table = soup.find('table',{'class':'wikitable plainrowheaders sortable'})

	data = []

	# Book title links to disregard
	book_links = ["/wiki/Snow_White","/wiki/The_Adventures_of_Pinocchio","/wiki/Bambi,_a_Life_in_the_Woods","/wiki/Peter_and_Wendy","/wiki/Cinderella","/wiki/The_Sorcerer%27s_Apprentice","/wiki/Rapunzel","/wiki/Donkey_Kong","/wiki/Pac-Man","/wiki/The_Snow_Queen","/wiki/Alice%27s_Adventures_in_Wonderland","/wiki/Through_the_Looking-Glass","/wiki/Casey_at_the_Bat","/wiki/Peter_and_the_Wolf","/wiki/Little_Bear_Bongo","/wiki/Jack_and_the_Beanstalk","/wiki/Little_Toot","/wiki/Trees_(poem)","/wiki/The_Wind_in_the_Willows","/wiki/The_Legend_of_Sleepy_Hollow","/wiki/Cinderella","/wiki/Alice%27s_Adventures_in_Wonderland","/wiki/Through_the_Looking-Glass","/wiki/Sleeping_Beauty","/wiki/The_Sleeping_Beauty_(ballet)","/wiki/The_Hundred_and_One_Dalmatians","/wiki/The_Sword_in_the_Stone_(novel)","/wiki/The_Jungle_Book","/wiki/Winnie-the-Pooh","/wiki/The_Rescuers_(book)","/wiki/The_Fox_and_the_Hound_(novel)","/wiki/The_Chronicles_of_Prydain","/wiki/Basil_of_Baker_Street","/wiki/Oliver_Twist","/wiki/The_Little_Mermaid","/wiki/Beauty_and_the_Beast","/wiki/Aladdin_and_the_Magic_Lamp","/wiki/One_Thousand_and_One_Nights","/wiki/The_Hunchback_of_Notre-Dame","/wiki/Ballad_of_Mulan","/wiki/Tarzan_of_the_Apes","/wiki/The_Steadfast_Tin_Soldier","/wiki/Treasure_Island","/wiki/Henny_Penny","/wiki/A_Day_with_Wilbur_Robinson","/wiki/The_Frog_Princess_(novel)","/wiki/The_Frog_Prince","/wiki/Big_Hero_6_(comics)"]

	movie_list = table.find_all("i")
	for i in movie_list:
		if i.a:
			link = i.a["href"]
			# Disregard links to book titles
			if link in book_links:
				continue
			else:
				data.append(link)

	# Get relevant info for each movie -------------------------------------------------------
	movie_dict = {}
	relevant_Info = ["Title","Release dates","Running time","Budget","Box office","Release date"]

	# Generate url for each film produced by the corresponding production company
	for x in data:
		url = "https://en.wikipedia.org"+x
		info_box = extract_movie_details(url)
		info = []
		for i in range(6):
			if i == 0:
				title = info_box["Title"]
				info.append(info_box[relevant_Info[i]])
			else:
				info.append(info_box[relevant_Info[i]])

			movie_dict[title]=info
			print(info)

	# Save acquired info into csv file
	with open (csvFile,'w') as file:
		writer = csv.writer(file)
		writer.writerow(relevant_Info)
		for x in movie_dict:
			writer.writerow(movie_dict[x])