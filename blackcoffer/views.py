from rest_framework.views import APIView
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.http import JsonResponse
import secrets
import random

def get_data(request):
    # connect to MongoDB database
    client = MongoClient('mongodb+srv://VaishaliSharath:W31NHKg9k1LSNIVU@cluster0.ocr2e.mongodb.net/?retryWrites=true&w=majority')
    db = client.blackoffer
    collection = db.test

    # get filter parameters from request
    end_year = request.GET.get('end_year')
    topic = request.GET.get('topic')
    sector = request.GET.get('sector')
    region = request.GET.get('region')
    pestle = request.GET.get('pestle')
    source = request.GET.get('source')
    swot = request.GET.get('swot')
    country = request.GET.get('country')
    city = request.GET.get('city')

    # build filter query
    filter_query = {}
    if end_year:
        filter_query['end_year'] = int(end_year)
    if topic:
        filter_query['topic'] = topic
    if sector:
        filter_query['sector'] = sector
    if region:
        filter_query['region'] = region
    if pestle:
        filter_query['pestle'] = pestle
    if source:
        filter_query['source'] = source
    if swot:
        filter_query['swot'] = swot
    if country:
        filter_query['country'] = country
    if city:
        filter_query['city'] = city

    # fetch data from collection
    data = []
    for doc in collection.find(filter_query):
        data.append(doc)

    data_list = []
    for item in data:
        item_dict = {
            'id': str(item['_id']),  # convert ObjectId to string
            "end_year": item['end_year'],
            "intensity": item['intensity'],
            "sector": item['sector'],
            "topic": item['topic'],
            "insight": item['insight'],
            "url": item['url'],
            "region": item['region'],
            "start_year": item['start_year'],
            "impact": item['impact'],
            "added": item['added'],
            "published": item['published'],
            "country": item['country'],
            "relevance": item['relevance'],
            "pestle": item['pestle'],
            "source": item['source'],
            "title": item['title'],
            "likelihood": ['likelihood']
        }

        data_list.append(item_dict)

    # return data as JSON response
    return JsonResponse({'data': data_list})

def clean_data():
    client = MongoClient(
        'mongodb+srv://VaishaliSharath:W31NHKg9k1LSNIVU@cluster0.ocr2e.mongodb.net/?retryWrites=true&w=majority')
    db = client.blackoffer
    collection = db.test

    # fetch data from collection
    data = []
    for doc in collection.find():
        data.append(doc)

    data_list = []
    for item in data:
        item_dict = {
            'id': str(item['_id']),  # convert ObjectId to string
            "end_year": item['end_year'],
            "intensity": item['intensity'],
            "sector": item['sector'],
            "topic": item['topic'],
            "insight": item['insight'],
            "url": item['url'],
            "region": item['region'],
            "start_year": item['start_year'],
            "impact": item['impact'],
            "added": item['added'],
            "published": item['published'],
            "country": item['country'],
            "relevance": item['relevance'],
            "pestle": item['pestle'],
            "source": item['source'],
            "title": item['title'],
            "likelihood": ['likelihood']
        }

        data_list.append(item_dict)

    df = pd.DataFrame(data_list)

    df['end_year'] = pd.to_numeric(df['end_year'], errors='coerce')
    df['impact'] = pd.to_numeric(df['impact'], errors='coerce')
    df['intensity'] = pd.to_numeric(df['intensity'], errors='coerce')
    df['likelihood'] = pd.to_numeric(df['likelihood'], errors='coerce')
    df['relevance'] = pd.to_numeric(df['relevance'], errors='coerce')
    df['start_year'] = pd.to_numeric(df['start_year'], errors='coerce')

    df['end_year'].fillna(0, inplace=True)
    df['impact'].fillna(0, inplace=True)
    df['intensity'].fillna(0, inplace=True)
    df['likelihood'].fillna(0, inplace=True)
    df['relevance'].fillna(0, inplace=True)
    df['start_year'].fillna(0, inplace=True)

    for col in df.columns:
        df.fillna('NaN', inplace=True)

    df['year_range_end'] = df['end_year'].apply(lambda x: str((x // 10)).split('.')[0] + "0's")
    df['year_range_start'] = df['start_year'].apply(lambda x: str((x // 10)).split('.')[0] + "0's")
    #print(df)

    return df

class ChartDataView(APIView):
    def get(self, request):
        data_frame = clean_data()
        param = request.query_params.get('param')

        if (len(data_frame[param].unique()) < 7):
            start = 0
            end = len(data_frame[param].unique())
            d_start = 0
            d_end = d_start
            p_start = 0
            p_end = p_start
            pl_start = 0
            pl_end = pl_start
        else:
            start = random.randint(0, len(data_frame[param].unique()) - 7)
            end = start + 7
            d_start = random.randint(0, len(data_frame[param].unique()) - 4)
            d_end = d_start + 4
            p_start = random.randint(0, len(data_frame[param].unique()) - 3)
            p_end = p_start + 3
            pl_start = random.randint(0, len(data_frame[param].unique()) - 5)
            pl_end = pl_start + 5

        ## Bar _ Line _ Radar Charts
        x_axis = data_frame[param].unique().tolist()[start:end]
        x = data_frame[param].value_counts()
        y = x.values.tolist()[start:end]
        labels = param
        bar_res = {
            'x_axis': x_axis,
            'title': labels,
            'color': '#' + secrets.token_hex(3),
            'y_axis': y
        }
        line_res = {
            'x_axis': x_axis,
            'title': labels,
            'color': '#' + secrets.token_hex(3),
            'y_axis': y
        }
        radar_res = {
            'x_axis': x_axis,
            'color': '#' + secrets.token_hex(3),
            'y_axis': y,
            'title': labels,
            'hover': '#' + secrets.token_hex(3),
        }

        ## Doughnut_Chart
        #data_frame = clean_data()

        d_x_axis = data_frame[param].unique().tolist()[d_start:d_end]
        d_x = data_frame[param].value_counts()
        d_y = d_x.values.tolist()[d_start:d_end]

        d_bg_color = ['#' + secrets.token_hex(3) for _ in range(4)]

        doughnut_res = {
            'x_axis': d_x_axis,
            'color': d_bg_color,
            'y_axis': d_y
        }

        ### Pie Chart

        #data_frame = clean_data()

        p_x_axis = data_frame[param].unique().tolist()[p_start:p_end]
        p_x = data_frame[param].value_counts()
        p_y = p_x.values.tolist()[p_start:p_end]

        p_bg_color = ['#' + secrets.token_hex(3) for _ in range(3)]
        p_hover_bg = ['#' + secrets.token_hex(3) for _ in range(3)]
        pie_res = {
            'x_axis': p_x_axis,
            'color': p_bg_color,
            'y_axis': p_y,
            'hover': p_hover_bg
        }

        #### Polar chart

        #data_frame = clean_data()

        pl_x_axis = data_frame[param].unique().tolist()[pl_start:pl_end]
        pl_x = data_frame[param].value_counts()
        pl_y = pl_x.values.tolist()[pl_start:pl_end]

        pl_bg_color = ['#' + secrets.token_hex(3) for _ in range(5)]
        polar_res = {
            'x_axis': pl_x_axis,
            'color': pl_bg_color,
            'y_axis': pl_y
        }

        res = {
            "bar_res": bar_res,
            "line_res": line_res,
            "radar_res": radar_res,
            "pie_res": pie_res,
            "polar_res": polar_res,
            "doughnut_res": doughnut_res
        }

        return JsonResponse(res)



def country_plot(request):
    country_df = clean_data()

    # create a dataframe with frequency of events by country
    country_freq = country_df.groupby('country').size().reset_index(name='frequency')

    # create the choropleth map
    fig = px.choropleth(country_freq, locations='country', locationmode='country names', color='frequency',
                        title='Frequency of Events by Country', color_continuous_scale='Blues')

    # convert the plot to JSON string
    plot_json = pio.to_json(fig)

    # return the plot as JSON response
    return JsonResponse({'plot': plot_json})
