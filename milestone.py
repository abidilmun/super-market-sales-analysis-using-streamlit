import pandas as pd
import plotly.express as px
import scipy.stats as sc
import streamlit as st

#functions
def tho2k(a):
    a = a[:len(a)-3]
    a = '$ '+a+'K'
    return a


#layout setting
st.set_page_config(layout = 'wide')


#sidebar
st.sidebar.title('PAGE')
page = st.sidebar.selectbox('',['Dashboard','Inferencial Analysis'])

if page == 'Dashboard':
	#loading data
	df = pd.read_csv('supermarket_sales - Sheet1.csv') 

	#converting Date and Time features
	df.Date = pd.to_datetime(df.Date)
	df.Time = pd.to_datetime(df.Time).dt.time

	#total sales calculation
	ts = df.Total
	ts.index = df.Date
	totalSales = df.Total.sum()
	totalSales = round(totalSales)
	totalSales = str(totalSales)

	#daily sales calculation
	ds = df.groupby('Date').agg('sum').Total.mean()
	dailySales = round(ds)
	dailySales = str(dailySales)

	#monthly sales calculation
	ms = df.groupby('Date').agg('sum')
	ms.index = ms.index.month
	ms['month'] = ms.index
	ms = ms.groupby('month').agg('sum')
	monthlySales = ms.Total.mean()
	monthlySales = round(monthlySales)
	monthlySales = str(monthlySales)

	#writing title
	col1, col2, col3 = st.columns([3,6,2])
	col2.title('ABC Mart 2019 Historical Sales')
	col2.title('')
	col2.title('')
	col2.title('')

	#line break
	st.markdown('<hr>',unsafe_allow_html=True)

	#making columns
	col1, col2, col3, col4, col5= st.columns([.5,1,1,1,1])

	#total sales column
	col2.markdown('### Total Sales')
	col2.markdown('#### '+tho2k(totalSales))
	#monthly sales column

	col3.markdown('### Monthly Sales')
	col3.markdown('#### '+tho2k(monthlySales))
	#daily sales column

	col4.markdown('### Daily Sales')
	col4.markdown('#### '+tho2k(dailySales))

	#Customer Rating
	col5.markdown('### Cust. Rating')
	col5.markdown('#### '+str(round(df.Rating.mean(),1)))
	st.markdown('<hr>',unsafe_allow_html=True)

	#widgets columns
	col1, col2 = st.columns(2)

	#creating df for date filters
	dff = df.copy()
	dff = dff.groupby('Date').agg('sum')

	#creating date filters
	startDate = col1.date_input('Start',dff.index.min())
	endDate = col2.date_input('End',dff.index.max())

	#giving line break
	st.markdown('<hr>',unsafe_allow_html=True)

	#creating 3 columns
	col1,col2,col3 = st.columns(3)
	branch = col1.selectbox('Branch',['Whole','A','B','C'])
	window = col2.slider('Window (higher the number, smoother the line)',0,30,0,1)
	feature = col3.multiselect('Performance Features',['gross income','cogs','Total'],['Total','cogs'])

	if branch != 'Whole':
		dff = df.copy()
		dff = dff[dff.Branch == branch]
		dff = dff.groupby('Date').agg('sum')
	else:
		pass
		
	#line chart	
	if window == 0:
		st.line_chart(dff[feature][str(startDate):str(endDate)],height = 400)
	else:
		st.line_chart(dff[feature][str(startDate):str(endDate)].rolling(window).mean(),height = 400)
		
	col1,col2,col3 = st.columns([4,0.5,4])
	
	if branch == 'Whole':
		time = df.groupby('Time').agg('mean')
		time['hour'] = [i.hour for i in time.index]
		time = time.groupby('hour').agg('mean')
		
		
		payment = df.groupby('Payment').agg('count')
		payment = payment/1000*100
		fig = px.pie(payment, values = 'Total', names = payment.index)

	else:
		time = df[df.Branch == branch].groupby('Time').agg('mean')
		time['hour'] = [i.hour for i in time.index]
		time = time.groupby('hour').agg('mean')
		
		payment = df[df.Branch == branch].groupby('Payment').agg('count')
		payment = payment/1000*100
		fig = px.pie(payment, values = 'Total', names = payment.index)
		
		
	col1.markdown('### Sales By Hour')
	col1.write('')
	col1.write('')
	col1.bar_chart(time.Total)
	
	col3.markdown('### Payment Method')
	col3.plotly_chart(fig)
	
	col1,col2, col3 = st.columns([1,2.4,3])
	if branch == 'Whole':
	
		gender = df.groupby('Gender').sum()
		gender = gender/gender.sum()*100
		line = df.groupby('Product line').sum()
	else:
		gender = df[df.Branch == branch].groupby('Gender').sum()
		gender = gender/gender.sum()*100
		line = df[df.Branch == branch].groupby('Product line').sum()
	
	fig = px.pie(gender, values = 'Total', names = gender.index)
	col1.markdown('### Customer Spending By Gender')
	col1.plotly_chart(fig)
	fig = px.bar(x = line.index, y = line.Total)
	col3.markdown('### Sales by Product Line')
	col3.plotly_chart(fig)
	
	with st.expander('Data Description'):
		st.markdown('''
			### Context

			The growth of supermarkets in most populated cities are increasing and market competitions are also high. The dataset is one of the historical sales of supermarket company which has recorded in 3 different branches for 3 months data. Predictive data analytics methods are easy to apply with this dataset.

			### Attribute information

			Invoice id: Computer generated sales slip invoice identification number

			Branch: Branch of supercenter (3 branches are available identified by A, B and C).

			City: Location of supercenters

			Customer type: Type of customers, recorded by Members for customers using member card and Normal for without member card.

			Gender: Gender type of customer

			Product line: General item categorization groups - Electronic accessories, Fashion accessories, Food and beverages, Health and beauty, Home and lifestyle, Sports and travel

			Unit price: Price of each product in $

			Quantity: Number of products purchased by customer

			Tax: 5% tax fee for customer buying

			Total: Total price including tax

			Date: Date of purchase (Record available from January 2019 to March 2019)

			Time: Purchase time (10am to 9pm)

			Payment: Payment used by customer for purchase (3 methods are available – Cash, Credit card and Ewallet)

			COGS: Cost of goods sold

			Gross margin percentage: Gross margin percentage

			Gross income: Gross income

			Rating: Customer stratification rating on their overall shopping experience (On a scale of 1 to 10)

			### Acknowledgements

			Thanks to all who take time and energy to perform Kernels with this dataset and reviewers.

			### Purpose

			This dataset can be used for predictive data analytics purpose.
		''')
else:
	#loading data
	df = pd.read_csv('supermarket_sales - Sheet1.csv') 

	#converting Date and Time features
	df.Date = pd.to_datetime(df.Date)
	df.Time = pd.to_datetime(df.Time).dt.time
	#writing title
	col1, col2, col3 = st.columns([3,6,2])
	col2.title('ABC Mart 2019 Historical Sales')

	
	#writing title
	col1, col2, col3 = st.columns([4.7,6,2])
	col2.markdown('## Inferencial Analysis')
	
	st.write(
		"""
		
		This part will conduct tests to take conlcusions extractable from the data. first of all, i would like to know whether 	
		the sales differ each month. as we can see from the visuals in the Dashboard page, they do not differ that much. 
		for a better conclusioni i would like to use ANOVA test to the three month samples together. if they differ significantly
		i will test the samples using one tailed z-test. the reason being sample size is more than 30 and i want to know if a
		particular month has better sales than the other.   

		
		"""
	)
	
	col1, col2 = st.columns([1,.5])
	col1.markdown('#### H0 : Sales are consistant each month')
	col2.markdown('#### H1 : Sales fluctuate each month')
	
	bul = [i.month for i in df.Date]
	statsdf = df[['Total','Branch']]
	statsdf['month'] = bul
	jan = statsdf[statsdf.month == 1]
	feb = statsdf[statsdf.month == 2]
	mar = statsdf[statsdf.month == 3]
	res = sc.f_oneway(jan.Total,feb.Total,mar.Total)
	st.markdown('<hr>',unsafe_allow_html = True)
	col1,col2,col3,col4 = st.columns([1,1,1,0.5])
	col2.markdown('### F-statistics')
	col3.markdown('### P-value')
	st.markdown('<hr>',unsafe_allow_html = True)
	col1,col2,col3,col4 = st.columns([1,1,1,0.4])
	col2.markdown(f'### {round(res[0],2)}')
	col3.markdown(f'### {round(res[1],2)}')
	st.markdown('<hr>',unsafe_allow_html = True)
	
	st.write(
		"""
		
		The result shows that the three months do not differ significantly as the p-value is way above alpha equals to 5%. then
		the null hypothesis stands still unbreakable. that concludes ABC mart sales from January to March seem to be consistant,
		they differ but insignificantly.
		if that's the case. we can not go further testing which month is better than the other as no month is, significantly.   
		this could be an early indication that the ABC mart's performance is stagnant throughout the months. and stagnancy most 
		of the time is not a prefered kind of perfomance. 
		"""
	)
	

	



