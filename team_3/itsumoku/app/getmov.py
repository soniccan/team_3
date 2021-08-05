from googleapiclient.discovery import build

from datetime import datetime, timedelta,timezone
import pandas as pd
import re
import numpy as np
import sys


def get_video_list_in_channel(youtube,during:int,keyword,max_req_cnt=2):

    '''特定チャンネルの動画情報一覧を取得し、必要な動画情報を返す
    
        公開時刻が新しい順に50ずつリクエスト
        デフォルトでは最大2リクエストで終了
    '''


    n_requested = 20


    earliest_publishedtime =\
        datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    req_cnt = 0
    result = []
    channel_id = 'UCd0pUnH7i5CM-Y8xRe7cZVg'
    while True:
        response = youtube.search().list(part='snippet',
                                        
                                        order='date',
                                        q= f'#もくもく会 {keyword}',
                                        type='video',
                                        publishedBefore=earliest_publishedtime,
                                        maxResults=n_requested).execute()

        
        req_cnt += 1
        video_info = fetch_video_info(response)
        result.append(video_info)
        
        # 取得動画の最も遅い公開日時の1秒前以前を次の動画一覧の取得条件とする
        last_publishedtime = video_info['publishTime'].min()
        last_publishedtime_next =\
            datetime.strptime(last_publishedtime, '%Y-%m-%dT%H:%M:%SZ') - timedelta(seconds=1)
        
        earliest_publishedtime = last_publishedtime_next.strftime('%Y-%m-%dT%H:%M:%SZ')

        if req_cnt > max_req_cnt:
            # リクエスト回数がmax_req_cntを超えたらループを抜ける
            print('Result count exceeded max count {}.'.format(max_req_cnt))
            break

        if len(response['items']) < n_requested:
            # リクエストした動画数より少ない数が返った場合はループを抜ける
            print('Number of results are less than {}.'.format(n_requested))
            break

    if len(result) > 1:
        df_video_list = pd.concat(result, axis=0).reset_index(drop=True)
    else:
        df_video_list = result[0]

    return df_video_list


def fetch_video_info(response, as_df=True):
    '''APIのレスポンスから必要な動画情報を抜き出す'''
    info_list = []
    for item in response['items']:
        info = {}
        info['title'] = item['snippet']['title']
        info['kind'] = item['id']['kind']
        info['videoId'] = item['id']['videoId']
        info['description'] = item['snippet']['description']
        info['publishTime'] = item['snippet']['publishTime']
        info['channelTitle'] = item['snippet']['channelTitle']
        info['thumbnails_url'] = item['snippet']['thumbnails']['default']['url']
        info_list.append(info)
    if as_df:
        return pd.DataFrame(info_list)
    else:
        info_list




def get_contents_detail_core(youtube, videoids):
    '''動画の詳細情報を取得'''
    part = ['snippet', 'contentDetails']
    response = youtube.videos().list(part=part, id=videoids).execute()
    results = []
    for item in response['items']:
        info = get_basicinfo(item)
        info['duration'] = get_duration(item)
        results.append(info)
    return pd.DataFrame(results)


def get_contents_detail(youtube, videoids):
    '''必要に応じて50件ずつにIDを分割し、詳細情報を取得'''
    n_req_pre_once = 50
    
    # IDの数が多い場合は50件ずつ動画IDのリストを作成
    if len(videoids) > n_req_pre_once:
        videoids_list = np.array_split(videoids, len(videoids) // n_req_pre_once + 1)
    else:
        videoids_list = [videoids,]

    # 50件ずつ動画IDのリストを渡し、動画の詳細情報を取得
    details_list = []
    for vids in videoids_list:
        df_video_details_part = get_contents_detail_core(youtube, vids.tolist())
        details_list.append(df_video_details_part)

    df_video_details = pd.concat(details_list, axis=0).reset_index(drop=True)
    return df_video_details


def get_duration(item):
    '''動画時間を抜き出す（ISO表記を秒に変換）'''
    content_details = item['contentDetails']
    pt_time = content_details['duration']
    return pt2sec(pt_time)


def get_basicinfo(item):
    '''動画の基本情報の抜き出し'''
    basicinfo = dict(id=item['id'])
    # snippets
    keys = ('title', 'description', 'channelTitle')
    snippets = {k: item['snippet'][k] for k in keys}
    basicinfo.update(snippets)
    return basicinfo


def pt2sec(pt_time):
    '''ISO表記の動画時間を秒に変換 '''
    pttn_time = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')
    keys = ['hours', 'minutes', 'seconds']
    m = pttn_time.search(pt_time)
    if m:
        kwargs = {k: 0 if v is None else int(v[:-1])
                    for k, v in zip(keys, m.groups())}
        return timedelta(**kwargs).total_seconds()
    # else:
        # msg = '{} is not valid ISO time format.'.format(pt_time)
        # raise ValueError(msg)
def exec_getmov(during:int,keyword):
    # 利用するAPIサービス
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    if keyword =='female':
        keyword='女'
    if keyword =='male':
        keyword='男'
    if keyword =='anime':
        keyword='アニメ'
    if keyword =='any':
        keyword =''
    


    # APIキー
    YOUTUBE_API_KEY = 'AIzaSyDfeKIUYj9A_LPzUggppcIMEJzec-4VvJU'

    # API のビルドと初期化
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY)   
    
    df_video_list = get_video_list_in_channel(youtube,during,keyword)
    videoids = df_video_list['videoId'].values
    
    df_video_details = get_contents_detail(youtube, videoids)

    diff = 8
    lower_duration = during - diff * 60  # 
    upper_duration = during + diff*60 #誤差はdiff分以内。 
    is_matched = df_video_details['duration'].between(lower_duration, upper_duration)
    df_video_playlist = df_video_details.loc[is_matched, :]

    df ="https://www.youtube.com/embed/"+df_video_playlist['id'].values
    return df

if __name__=='__main__':
    during = 30*60
    keyword ="male"
    exec_getmov(during,keyword)