#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import json
import sqlite3
import html

class Get_detail(object):
    ''' Get moods detail information and save it to database'''

    def __init__(self, conn, cur):
        self.count = 0
        self.conn = conn
        self.cur = cur

    def make_dict(self):
        mood_dict = dict()
        dir_list = os.listdir('mood_result')
        for d in dir_list:
            file_list = os.listdir('mood_result/' + d)
            if len(file_list) != 1:
                mood_dict[d] = file_list
        return mood_dict

    def exact_mood_data(self, qq, fname):
        '''Get mood data from files in result folder
        '''

        qqnumber = qq
        filename = fname
        with open(filename) as f:
            con = f.read()
        con_dict = json.loads(con[10:-2])
        try:
            moods = con_dict['msglist']
        except KeyError:
            return
        if moods == None:
            return

        mood_item = dict()
        mood_item['belong'] = qqnumber

        for mood in moods:
            mood_item['content'] = mood['content']
            mood_item['create_time'] = mood['created_time']
            mood_item['comment_num'] = mood['cmtnum']
            mood_item['phone'] = mood['source_name']
            mood_item['pic'] = mood['pic'][0]['url2'] if 'pic' in mood else ''
            mood_item['locate'] = mood['story_info']['lbs']['name'] if 'story_info' in mood else ''

            if mood_item['content'] == '' and mood_item['pic'] != '':
                # if the mood only has pic but no other thing
                mood_item['content'] = mood_item['pic']
            if mood_item['content'] == '' and 'rt_con' in mood:
                # if the mood is a forward video
                # it will be in the mood['rt_con']
                try:
                    mood_item['content'] = mood['rt_con']['conlist'][0]['con']
                except IndexError:
                    mood_item['content'] = mood['rt_con']['conlist'][1]['con']
                except KeyError:
                    # when the mood only has a link
                    mood_item['content'] = mood['rt_con']['content']
                except TypeError:
                    # when the mood only has a video
                    mood_item['content'] = mood['video'][0]['url3']

            print('Dealing with %d' % self.count)
            self.insert_to_db(mood_item)
            self.count += 1
            if self.count % 1000 == 0:
                self.conn.commit()

    def insert_to_db(self, mood):
        sql = 'INSERT INTO moods (qq, ctime,  content, comment_count, phone, image, locate) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.cur.execute(sql, (mood['belong'], mood['create_time'], mood['content'], mood['comment_num'], mood['phone'], mood['pic'], mood['locate']))


if __name__ == '__main__':

    conn = sqlite3.connect('moods.sqlite')
    cur = conn.cursor()

    app = Get_detail(conn, cur)
    mood_dict = app.make_dict()

    for dirname, fname in mood_dict.items():
        for each_file in fname:
            filename = os.path.join('mood_result', dirname, each_file)
            app.exact_mood_data(dirname, filename)
    else:
        conn.commit()
        cur.close()
        conn.close()
        print('Finish!')
