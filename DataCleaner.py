
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler


class DataCleaner(object):
    """
    Data Cleaning Class object. As of version 1.0, user creates  a dictionary of fields, and operations to perform on fields, and applies those operations to a dataframe.
    """
    def __init__(self):
        '''
        fld_info_dict: Dictionary of string, string pairs. Each key is the name of the field/column, and the value is the operation to be performed.

        Operations:
        'drop' : Drop the given fields from the DataFrame.
        'label' : Removes label column from frame, and stores separately.
        'dummie' : Turns column into multiple dummy columns to add on to DataFrame
        'boolean' : Modifies column to booleans with specified values. Ex.'gender' : 'boolean={male:1,female:0}' would change a column named 'gender' in a DataFrame to a column that contained 1s and 0s for the males and females respectively.
        'date' : change to date.
        'fillna' : fill missing values in column with given values
            ie 'fillna=0'
        '''
        self.fld_info_dict = {
            'fraud': 'label',
            'acct_type':'drop',
            'approx_payout_date': 'drop',
            'body_length' : '',
            'channels' : '',
            'country' : 'dummie',
            'currency' : 'dummie',
            'delivery_method' : 'dummie',
            'description' :'drop',
            'email_domain' :'drop',
            'event_created' : 'drop',
            'event_end' : 'drop',
            'event_published': 'drop',
            'event_start' : 'drop',
            'fb_published' : 'drop',
            'gts' : 'drop',
            'has_analytics' :  'fillna=0',
            'has_header':  'fillna=0',
            'has_logo':  'fillna=0',
            'listed' : 'boolean={y:1,n:0}',
            'name': 'drop',
            'name_length': 'drop',
            'num_order':  'drop',
            'num_payouts': '',
            'object_id' : 'drop',
            'org_desc' : 'drop',
            'org_facebook' : 'drop',
            'org_name' : 'drop' ,
            'org_twitter': 'drop',
            'payee_name': 'drop',
            'payout_type': 'drop',
            'previous_payouts' : 'drop',
            'sale_duration' : 'drop',
            'sale_duration2' : 'drop',
            'show_map' : 'drop',
            'ticket_types' : 'drop',
            'user_age' : 'drop',
            'user_created' : 'drop',
            'user_type' : '',
            'venue_address' : 'drop',
            'venue_country' : 'drop',
            'venue_latitude' : 'drop',
            'venue_longitude' : 'drop',
            'venue_name' : 'drop',
            'venue_state' : 'drop'
            }

        self.dummy_dict = {}
        self.std_scaler = None


    def clean(self, df):
        '''
        Takes a Pandas DataFrame and does the modifications specified in the Initalize
        Returns a matrix of X vlaues
        if label field exists returns NP matrix of X and the y values
        X,y format.
        '''

        '''Create new fields for differnce in time'''
        df['date_diff'] = df['event_end'] - df['user_created']
        df['date_diff2'] = df['event_start'] - df['event_created']
        y_vals=False

        ## Need to add functionality to modify the df somehow

        for fld, funct in self.fld_info_dict.iteritems():
            if fld not in df.columns.values:
                continue
            elif funct == 'drop':  #drop field
                df.drop(fld, inplace=True, axis=1)

            elif funct == 'label':
                if fld in df.columns.values:
                    y = df.pop(fld)
                    y_vals=True

            elif funct == 'dummie':
                '''Makes the dummies for the given fields.  Saves the fields used in a dummy dictionary to compare when testing files are cleaned. '''
                dumbs = pd.get_dummies(df[fld], prefix = fld+'_', dummy_na=True)
                if self.dummy_dict.get(fld) == None:
                    self.dummy_dict[fld]=dumbs.columns.values
                else:
                    dumbs = self._test_check_dumbs(dumbs,self.dummy_dict.get(fld))

                df = pd.concat([df, dumbs], axis=1)
                df.drop(fld, inplace=True, axis=1)

            elif funct.split('=')[0] == 'boolean':
                blvl = funct.split('=')[1]
                items = blvl.strip('{}').split(',')
                pairs = [item.split(':',1) for item in items]
                boolean_dict = dict((k,eval(v)) for (k,v) in pairs)
                df[fld] = df[fld].map(boolean_dict)

            elif funct == 'date':
                df[fld] =  pd.to_datetime(df[fld],unit='s')

            elif funct.split('=')[0] == 'fillna':
                na_fill_val = funct.split('=')[1]
                df[fld].fillna(na_fill_val,inplace=True)

        if y_vals:
            return df, y
        else:
            return df


    def _test_check_dumbs(self, temp,temp2):
        '''Internal use. Takes the given column and makes sure any dummie dictionarys have all the same fields. (usally used when trying to predict.)'''
        for i in temp2:
            if i not in temp.columns.values:
                temp[i]=np.zeros(temp.shape[0])
        for i in temp.columns.values:
            if i not in temp2:
                temp.drop(i, axis = 1, inplace = True)
        return temp


    def normalize_data(self, X):
        '''
        call and pass in data to normalize X data.
        keeps track of the StandardScaler so you dont need to
        '''
        if self.std_scaler == None:
            self.std_scaler = StandardScaler()
            self.std_scaler.fit(X)
        return self.std_scaler.transform(X)
