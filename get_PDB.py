from email.quoprimime import header_check
from ssl import HAS_NEVER_CHECK_COMMON_NAME
import pandas as pd
import datetime as dt
import rcsbsearch
from rcsbsearch import rcsb_attributes as attrs


###########################################################################
# Get lists of terms with pandas. Need to add valid path...

try:
    search_terms_df = pd.read_excel(PATH_GOES_HERE)
    '''
    "C:\Users\mryan\OneDrive\Documents\Workflow Informatics\Nimbus\Projet PDB Search Terms.xlsx"
    '''
except:
    print('path to search terms not found')


term_dict = {}
for i in range(0,len(search_terms_df.index)):
    term_dict[search_terms_df.loc[i,'Target']]= search_terms_df.loc[i,'Search Words']

for k in term_dict:
    #print(k)
    #print (term_dict[k])

    term_dict[k] = term_dict[k].rsplit(';')

    for count in range(0,len(term_dict[k])):
        term_dict[k][count] = term_dict[k][count].strip()
    
    
    
    upper_list = [i.upper() for i in term_dict[k]]
    lower_list = [i.lower() for i in term_dict[k]]
    term_dict[k].extend(upper_list)
    term_dict[k].extend(lower_list)
    

#########################################################################
# Get 'from' and 'to' dates with datetime


dateNow = dt.datetime.now()

# change back to -7!
td = dt.timedelta(days=-1000)

dateThen = dateNow + td

todate = dateNow.strftime("%Y-%m-%d")
fromdate = dateThen.strftime("%Y-%m-%d")

daterange = [fromdate, todate]

#print(daterange)


############################################################################
# Forming terminals for each query, use BITWISE operators to combine

for i in term_dict:
    term1 = attrs.rcsb_accession_info.deposit_date.range(daterange)
    #print(i)
    entry_list = []
    for j in range(0,len(term_dict[i])):
        
        term2 = attrs.struct.title.contains_phrase(term_dict[i][j])

        full_query = term1 & term2

        #print(full_query)

        for entry in full_query('entry'):
            #print(entry)
            entry_list.append(entry)
    # NEED to filter duplicates
    print(i + ': ' + ','.join(entry_list))

    #print('END \n\n')
