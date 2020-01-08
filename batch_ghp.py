import pandas as pd
import numpy as np
from pathos.multiprocessing import Pool
import requests
import time
import json
import getpass
import pysftp
import dask.dataframe as dd
# Get Password for HPC
#pwd = getpass.getpass()
#Establish Connection with HPC
base_url = 'http://localhost:8989/route/?'
options = {
    'locale': 'en-US',
    'vehicle': 'car',
    'weighting': 'fastest',
    'elevation': 'false',
    'use_miles': 'true',
    'points_encoded': 'false',
    'simplify': 'true',
    'details': 'street_name'
}

#dr = '/Volumes/Fleet Storage/evan_build/OnePlusMegaWatt/route_jsons/'


def haversine(lon, lat):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees as vectors)
    """
    # convert decimal degrees to radians
    lon, lat = map(np.radians, [lon, lat])

    # haversine formula
    dlon = lon[1:] - lon[:-1]
    dlat = lat[1:] - lat[:-1]
    a = np.sin(
        dlat / 2)**2 + np.cos(lat[1:]) * np.cos(lat[:-1]) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 3965  # Radius of earth in kilometers. Use 3956 for miles
    return np.r_[0., c * r]


def res2csv(res, vid):
    df = pd.DataFrame(res['paths'][0]['points']['coordinates'],
                      columns=['lon', 'lat'])
    df['datetime'] = np.nan
    wptm = res['paths'][0]['waypoints_time']
    wps = [k for k in wptm.keys()]
    df.loc[wps, ['datetime']] = np.c_[wps]
    df.replace({'datetime': wptm}, inplace=True)
    df['datetime'] = pd.to_datetime(df.datetime, format='%Y-%m-%d %H:%M:%S')
    df['name'] = 0
    names = [res['paths'][0]['details']['street_name']][0]
    df.loc[np.array(names)[:, 0].astype(int), ['name']] = np.array(
        names)[:, 2].astype(int)
    df['name'].replace(to_replace=0, method='ffill', inplace=True)
    # pts = res['paths'][0]['points']['coordinates']
    df['distance_mi'] = haversine(df.lon.values, df.lat.values)
    # df.loc[df.datetime.str.contains(':').isna()] == np.nan

    df['total_time'] = df.index.map({
        inst['interval'][0]: inst['time'] / 1E3
        for inst in res['paths'][0]['instructions'] if inst['time'] > 0
    })
    df['total_distance'] = df.index.map({
        inst['interval'][0]: inst['distance'] / 1E3 / 1.60934
        for inst in res['paths'][0]['instructions'] if inst['time'] > 0
    })
    # {inst['interval'][0]:inst['time']/1E3 for inst in res['paths'][0]['instructions']}

    df['total_time'].ffill(inplace=True)
    df['total_distance'].ffill(inplace=True)

    df['dt'] = df.total_time * df.distance_mi / df.total_distance
    datetime = df.datetime.values
    for i, row in df.iterrows():
        if row['datetime'] is pd.NaT:
            datetime[i] = datetime[i - 1] + np.timedelta64(
                int(np.round(row['dt'] * 1E3)), 'ms')
    df['datetime'] = datetime
    df['speed_mph'] = df.distance_mi / df.dt * 3600
    df['vid'] = vid
    #df.to_csv('/Volumes/Fleet Storage/evan_build/OnePlusMegaWatt/Longhaul2/' +
    #          str(vid) + '.csv',
    #          index=False)
    df.to_csv('/data/mbap_shared/opmw/' + str(vid) + '.csv',index = False)
   

def make_request(gb):
    nm, gb = gb
    print(nm)
    gb['MESSAGE_DATE_TIME'] = pd.to_datetime(gb['MESSAGE_DATE_TIME'])
    gb = gb.sort_values(by=['MESSAGE_DATE_TIME']).reset_index(drop=True)
    gb['distance'] = gb['MILEAGE'].diff().fillna(10)
    gb = gb[gb['distance'] > 5].reset_index(drop=True)
    url = base_url + '&'.join([
        'point=' + str(x) + ',' + str(y)
        for x, y in gb[['LATITUDE', 'LONGITUDE']].values
    ])
    r = requests.get(url, params=options)
    if r.status_code == 400:
        try:
            gb = gb.drop([err['point_index']
                          for err in r.json()['hints']]).reset_index(drop=True)
        except:
            return 0
        url = base_url + '&'.join([
            'point=' + str(x) + ',' + str(y)
            for x, y in gb[['LATITUDE', 'LONGITUDE']].values
        ])
        r = requests.get(url, params=options)
    try:
        res = r.json()
        datetimes = gb['MESSAGE_DATE_TIME'].tolist()
        wptm = {0: str(datetimes.pop(0))}
        wptm.update({
            inst['interval'][0]: str(datetimes.pop(0))
            for inst in res['paths'][0]['instructions'] if inst['time'] == 0
        })
        tmp = res['paths'][0].copy()
        tmp.update({'waypoints_time': wptm})
        res['paths'][0] = tmp
        # with open(dr + str(nm) + '.json', 'w') as f:
        #     json.dump(res, f)
        res2csv(res, nm)
    except (KeyError, json.decoder.JSONDecodeError, IndexError):
        return 0

    if r.status_code == 200:
        return 1
    else:
        return 0


def main():
    from dask.diagnostics import ProgressBar
    ProgressBar().register()
    p = Pool(8)
    data_long = dd.read_csv('../NREL_Locations_clean.csv').compute()
    results = p.map_async(make_request,
                  [gb for gb in data_long.groupby('VIN_ID')]).get()
    print('total vehicles: ', np.sum(results))


if __name__ == '__main__':
    tic = time.time()
    main()
    toc = time.time()
    print('Total Elapsed Processing time: ', (toc - tic) / 60, ' mins')
