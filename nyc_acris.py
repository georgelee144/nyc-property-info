import requests
import pandas as pd
import time
import random

URL = 'https://a836-acris.nyc.gov/DS/DocumentSearch/BBLResult'
HEADER = {'User-Agent': 'Mozilla/5.0',
       'referer':'http://a836-acris.nyc.gov/bblsearch/bblsearch.asp'}

BOROUGH_NAME_VAULE_PAIRS = {    
                                 1:'MANHATTAN / NEW YORK'
                                ,2:'BRONX'
                                ,3:'BROOKLYN / KINGS'
                                ,4:'QUEENS'
                                ,5:'STATEN ISLAND / RICHMOND'
                                }

def get_home_by_bbl(**kwargs):
    
    # borough_name = kwargs.get('borough_name',None)
    borough = kwargs.get('borough',None)

    # borough = BOROUGH_NAME_VAULE_PAIRS.get(borough_name,None)

    #for coops only
    unit = kwargs.get('unit','')

    #vaild selectdate values is DR:date_range, 5Y:last 5 years, 2Y:last 2 years, 1Y:last 1 year, 90:last 90 days, 30: last thirty days, 7:last 7 days
    selectdate = kwargs.get('select_date','To Current Date') 

    block =  kwargs.get('block',None)

    lot =  kwargs.get('lot',0)

    #vaild doc_type values: 'ALL_MORT','ALL_DEED'
    doc_type = kwargs.get('doc_type','All Document Classes')

    #defaults to 10 rows
    max_rows = kwargs.get('max_rows',None)

    sleep = kwargs.get('sleep',True)
    # lot_value = str(lot)
    # if len(lot_value) < 4:
    #     for zero_to_lpad in 4-len(lot_value):
    #         lot_value = '0' + lot_value


# <input type="hidden" name="hid_datefromm" value="">
# <input type="hidden" name="hid_datefromd" value="">
# <input type="hidden" name="hid_datefromy" value="">
# <input type="hidden" name="hid_datetom" value="">
# <input type="hidden" name="hid_datetod" value="">
# <input type="hidden" name="hid_datetoy" value="">

    payload = {
            #  'hid_borough_name': borough_name
            'hid_borough':borough
            ,'hid_block':block
            # ,'hid_block_value':block_value
            ,'hid_lot':lot
            # ,'hid_lot_value':lot_value
            ,'hid_unit':unit
            ,'hid_doctype': doc_type
            ,'hid_page': 1
            ,'hid_max_rows':max_rows
            ,'hid_selectdate':selectdate

            ,'hid_SearchType': 'BBL'
            ,'hid_ISIntranet': 'N'
            ,'hid_sort': ''
            }

    response = requests.get(URL,headers=HEADER,params=payload)
    
    #sleep to not be rate limited
    if sleep:
        time.sleep(random.uniform(0,2))

    return response

def get_property_info(borough=None,block=None,lot=None,doc_type=None,unit=None,max_rows=None,selectdate=None):

    '''
    hard coded skips and indexs
    '''

    response = get_home_by_bbl(borough=borough,block=block,lot=lot,doc_type=doc_type,unit=unit,max_rows=max_rows,selectdate=selectdate)

    df = pd.read_html(response.text,skiprows=[0,1,2,3])[0]


    df.columns = ['View','Reel/Pg/File','CRFN','Lot ',' Partial ','Doc Date','Recorded / Filed','Document Type','Pages','Party1','Party2','Party 3/ Other','More Party','Corrected/','Doc Amount',]

    df = df[['CRFN','Lot ',' Partial ','Doc Date','Recorded / Filed','Document Type','Pages','Party1','Party2','Party 3/ Other','More Party','Corrected/','Doc Amount']]
    
    # df.sort_values(by=['Doc Date'],ascending=False,inplace=True)

    return df