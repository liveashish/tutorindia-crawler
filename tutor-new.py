from bs4 import BeautifulSoup
import re
import requests
import MySQLdb
import xlsxwriter




r  = requests.get('http://tutorindia.net/Personal_Tutor-online')
root = 'http://tutorindia.net'
data = r.text

soup = BeautifulSoup(data)
url_subject = raw_input("Enter URL of the subject: ")
start_page = int(raw_input("Enter start Page: "))
last_page = int(raw_input("Enter Last Page: "))

page_name = raw_input("Name of the Excel sheet: ")
count_id = 1;
row = 1
col = 0


# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('online_tutors-'+page_name+'.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
# Write some data headers.
worksheet.write('A1', 'ID', bold)
worksheet.write('B1', 'Name', bold)
worksheet.write('C1', 'Description', bold)
worksheet.write('D1', 'Subject', bold)
worksheet.write('E1', 'Phone', bold)
worksheet.write('F1', 'Education', bold)
worksheet.write('G1', 'Gender', bold)
worksheet.write('H1', 'Address', bold)
worksheet.write('I1', 'Locality', bold)
worksheet.write('J1', 'Region', bold)
worksheet.write('K1', 'PIN Code', bold)


for links in range(start_page, last_page+1):
	percentage_x = float(100/last_page)
	percentage = float(percentage_x/25)
	pagination = url_subject+'-p'+str(links)
	print '########################'
	print pagination
	print '########################'
	page_holder =  requests.get(pagination)
	data_page_holder = page_holder.text
	soup_page_holder = BeautifulSoup(data_page_holder)
	for profile_link in soup_page_holder.select('div.boxx a[href^=Tutor_Profiles-]'):
		
		final_profile_link = root+'/'+profile_link.get('href')
		q = requests.get(final_profile_link)
		data_q = q.text
		soup_q = BeautifulSoup(data_q)
		try:
			name = soup_q.find('span', {'itemprop': 'name'}).text
		except:
			pass
		try:
			description = soup_q.find('span', {'itemprop': 'description'}).text
		except:
			pass
		try:
			subject = soup_q.find('span', {'itemprop': 'subjects'}).text
		except:
			pass
		try:
			qualification = soup_q.find('span', {'itemprop': 'education'}).text
		except:
			pass
		try:
			gender = soup_q.find('span', {'itemprop': 'gender'}).text
		except:
			pass
		try:
			address = soup_q.find('span', {'itemprop': 'streetAddress'}).text
		except:
			pass
		try:
			locality = soup_q.find('span', {'itemprop': 'addressLocality'}).text
		except:
			pass
		try:
			region = soup_q.find('span', {'itemprop': 'addressRegion'}).text
		except:
			pass
		try:
			pin_code = soup_q.find('span', {'itemprop': 'postalCode'}).text
		except:
			pass
		try:
			phone = soup_q.find('span', {'itemprop': 'telephone'}).text
		except:
			pass
		print 'name :', name
		print 'des: ', description
		print 'subject: ', subject
		print 'qual: ', qualification
		print 'gender: ', gender
		print 'address: ', address
		print 'locality: ', locality
		print 'region: ', region
		print 'pin code: ', pin_code
		print 'phone: ', phone
		print '*************************************** ' + str(count_id*percentage) + '%'+' completed'
		
		worksheet.write(row, col, count_id)
		worksheet.write(row, col+1, name)
		worksheet.write(row, col+2, description)
		worksheet.write(row, col+3, subject)
		worksheet.write(row, col+4, phone)
		worksheet.write(row, col+5, qualification)
		worksheet.write(row, col+6, gender)
		worksheet.write(row, col+7, address)
		worksheet.write(row, col+8, locality)
		worksheet.write(row, col+9, region)
		worksheet.write(row, col+10, pin_code)

		row += 1
		
		# query = "INSERT INTO tutors_online (ID, Name, Description, Subject, Phone, Education, Gender, Address, Locality, Region, PIN Code) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (count_id, name, description, subject, phone, qualification, gender, address, locality, region, pin_code)
		# cursor.execute(query)
		# # Close the cursor
		# cursor.close()

		# # Commit the transaction
		# database.commit()
		count_id = count_id + 1

workbook.close()
print count_id + ' data scrapped and saved successfully' 
