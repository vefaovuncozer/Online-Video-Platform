import PySimpleGUI as sg
import sqlite3
from datetime import date
from datetime import datetime
import calendar
from random import randint
conn = sqlite3.connect('ProjectBackup.db')
c = conn.cursor()

def videoPage(videoid,in_userid,func):
    videoViewCount = c.execute("SELECT view_count FROM Video WHERE videoid = " + str(videoid) )
    videoViewCount = videoViewCount.fetchone()
    videoViewCount = videoViewCount[0]
    newVideoViewCount = videoViewCount +  1
    update = "UPDATE Video SET view_count = " + str(newVideoViewCount)+ " WHERE videoid = " + str(videoid)
    c.execute(update)
    conn.commit()
    
    video_single = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id,description,like_count,dislike_count FROM Video WHERE videoid = '" + str(videoid) + "'" )
    video_single = video_single.fetchone()
    video_upload = c.execute("SELECT upload_date FROM Video_Upload WHERE videoid = " + str(videoid))
    video_upload = video_upload.fetchone()
    seperation = video_upload[0].split("-")
    month = calendar.month_name[int(seperation[1])]
    dateformat = str(seperation[2]) + " " + month + " " +str(seperation[0])

    likeEvent = c.execute("SELECT status FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid))
    likeEvent = likeEvent.fetchone()
    likeButton = sg.Button('Like',button_color = "red")
    dislikeButton = sg.Button('Dislike',button_color = "red")
    if likeEvent:
        status = likeEvent[0]
        if status == "like":
            likeButton = sg.Button('Like',button_color = "gray")
            dislikeButton = sg.Button('Dislike',button_color = "red")
        if status == "dislike":
            dislikeButton = sg.Button('Dislike',button_color = "gray")
            likeButton = sg.Button('Like',button_color = "red")

        
    layout = [[sg.Text(str(video_single[1])),sg.Text("Duration: " + str(video_single[3])),sg.Text("Type: "+str(video_single[2]))],
              [sg.Text("Uploaded by: " + str(video_single[0])),sg.Text("Uploaded on: " + dateformat)],
              [sg.Text("Description: " + str(video_single[6]))],
              [sg.Text("Views: " + str(video_single[4])),sg.Text("Likes: "),sg.Text(str(video_single[7]),key="likeCountText"),sg.Text("Dislikes: "),sg.Text(str(video_single[8]),key="dislikeCountText"), likeButton,dislikeButton],
              [sg.Button('Back'),sg.Button('Exit')]]
    
    window = sg.Window(str(video_single[1]), layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
    
        if event == "Back":    
            if func == "Standard":
                window.close()
                windowStandard(in_userid)
            if func == "Partner":
                window.close()
                windowPartner(in_userid)
            break

        likeEvent = c.execute("SELECT status FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid))
        likeEvent = likeEvent.fetchone()
        if likeEvent:
            print(1)
            status = likeEvent[0]
            if status == "like":
                print(2)
                if event == "Like":
                    print(3)
                    window["Like"].update('Like',button_color = "red")
                    window["Dislike"].update('Dislike',button_color = "red")
                    videoLikeCount = c.execute("SELECT like_count FROM Video WHERE videoid = " + str(videoid) )
                    videoLikeCount = videoLikeCount.fetchone()
                    videoLikeCount = videoLikeCount[0]
                    newVideoLikeCount = videoLikeCount -  1

                    update = "UPDATE Video SET like_count = " + str(newVideoLikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    update_likeTable = "DELETE FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid)
                    c.execute(update_likeTable)
                    conn.commit()  
                    window["likeCountText"].update(newVideoLikeCount)
                
                if event == "Dislike":
                    print(4)
                    window["Like"].update('Like',button_color = "red")
                    window["Dislike"].update('Dislike',button_color = "gray")
                    videoLikeCount = c.execute("SELECT like_count FROM Video WHERE videoid = " + str(videoid) )
                    videoLikeCount = videoLikeCount.fetchone()
                    videoLikeCount = videoLikeCount[0]
                    newVideoLikeCount =videoLikeCount -  1
                    update = "UPDATE Video SET like_count = " + str(newVideoLikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    update_likeTable = "UPDATE LikeDislike SET status = 'dislike' WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid)
                    c.execute(update_likeTable)
                    conn.commit()  
                    videoDislikeCount = c.execute("SELECT dislike_count FROM Video WHERE videoid = " + str(videoid)  )
                    videoDislikeCount = videoDislikeCount.fetchone()
                    videoDislikeCount = videoDislikeCount[0]
                    newVideoDislikeCount = videoDislikeCount + 1
                    update = "UPDATE Video SET dislike_count = " + str(newVideoDislikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    window["likeCountText"].update(newVideoLikeCount)
                    window["dislikeCountText"].update(newVideoDislikeCount)
                
            if status == "dislike":
                print(5)
                if event == "Dislike":
                    print(6)
                    window["Dislike"].update('Dislike',button_color='red')
                    window["Like"].update('Like', button_color = "red")
                    videoDislikeCount = c.execute("SELECT dislike_count FROM Video WHERE videoid = " + str(videoid) )
                    videoDislikeCount = videoDislikeCount.fetchone()
                    videoDislikeCount = videoDislikeCount[0]
                    newVideoDislikeCount = videoDislikeCount - 1
                    
                    update = "UPDATE Video SET dislike_count = " + str(newVideoDislikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    update_likeTable = "DELETE FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid)
                    c.execute(update_likeTable)
                    conn.commit()
                    window["dislikeCountText"].update(newVideoDislikeCount)
                    
                if event == "Like":
                    print(7)
                    window["Dislike"].update('Dislike',button_color='red')
                    window["Like"].update('Like',button_color = "gray")
                    videoDislikeCount = c.execute("SELECT dislike_count FROM Video WHERE videoid = " + str(videoid)  )
                    videoDislikeCount = videoDislikeCount.fetchone()
                    videoDislikeCount = videoDislikeCount[0]
                    newVideoDislikeCount = videoDislikeCount -  1
                    update = "UPDATE Video SET dislike_count = " + str(newVideoDislikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    update_likeTable = "UPDATE LikeDislike SET status = 'like' WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid)
                    c.execute(update_likeTable)
                    conn.commit()  
                    videoLikeCount = c.execute("SELECT like_count FROM Video WHERE videoid = " + str(videoid))
                    videoLikeCount = videoLikeCount.fetchone()
                    videoLikeCount = videoLikeCount[0]
                    newVideoLikeCount = videoLikeCount + 1
                    update = "UPDATE Video SET like_count = " + str(newVideoLikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit() 
                    window["likeCountText"].update(newVideoLikeCount)
                    window["dislikeCountText"].update(newVideoDislikeCount)
            if status != "like" and status != "dislike" : 
                print(8)
                if event == "Like":
                    print(9)
                    window["Like"].update('Like',button_color = "gray")
                    window["Dislike"].update('Dislike',button_color='red')
                    videoLikeCount = c.execute("SELECT like_count FROM Video WHERE videoid = " + str(videoid) )
                    videoLikeCount = videoLikeCount.fetchone()
                    videoLikeCount = videoLikeCount[0]
                    newVideoLikeCount = videoLikeCount +  1
                    update = "UPDATE Video SET like_count = " + str(newVideoLikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    likeEvent = c.execute("SELECT videoid FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid) + " and status IN ('like','dislike')"    )          
                    likeEvent = likeEvent.fetchone()
                    if not likeEvent:
                        print(10)
                        insert = "INSERT INTO LikeDislike (videoid, user_id, status) VALUES (" + str(videoid) + ", " + str(in_userid) + ", 'like');"
                        c.execute(insert)
                        conn.commit()
                    window["likeCountText"].update(newVideoLikeCount)
                    
                if event == "Dislike":
                    print(11)
                    window["Dislike"].update('Dislike',button_color = "gray")
                    window["Like"].update('Like',button_color='red')
                    videoDislikeCount = c.execute("SELECT dislike_count FROM Video WHERE videoid = " + str(videoid) )
                    videoDislikeCount = videoDislikeCount.fetchone()
                    videoDislikeCount = videoDislikeCount[0]
                    newVideoDislikeCount = videoDislikeCount +  1
                    update = "UPDATE Video SET dislike_count = " + str(newVideoDislikeCount)+ " WHERE videoid = " + str(videoid)
                    c.execute(update)
                    conn.commit()
                    likeEvent = c.execute("SELECT videoid FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid)+ " and status IN  ('like','dislike')")
                    likeEvent = likeEvent.fetchone()
                    if not likeEvent:
                        print(12)
                        insert = "INSERT INTO LikeDislike (videoid, user_id, status) VALUES (" + str(videoid) + ", " + str(in_userid) + ", 'dislike');"
                        c.execute(insert)
                        conn.commit()
                    window["dislikeCountText"].update(newVideoDislikeCount)  
        else:    
            print(13)
            if event == "Like":
                print(14)
                window["Like"].update('Like',button_color = "gray")
                window["Dislike"].update('Dislike',button_color = "red")
                videoLikeCount = c.execute("SELECT like_count FROM Video WHERE videoid = " + str(videoid) )
                videoLikeCount = videoLikeCount.fetchone()
                videoLikeCount = videoLikeCount[0]
                newVideoLikeCount = videoLikeCount +  1
                update = "UPDATE Video SET like_count = " + str(newVideoLikeCount)+ " WHERE videoid = " + str(videoid)
                c.execute(update)
                conn.commit()
                likeEvent = c.execute("SELECT videoid FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid) + " and status IN ('like','dislike')"    )          
                likeEvent = likeEvent.fetchone()
                if not likeEvent:
                    print(15)
                    insert = "INSERT INTO LikeDislike (videoid, user_id, status) VALUES (" + str(videoid) + ", " + str(in_userid) + ", 'like');"
                    c.execute(insert)
                    conn.commit()
                window["likeCountText"].update(newVideoLikeCount)
                
            if event == "Dislike":
                print(16)
                window["Dislike"].update('Dislike',button_color = "gray")
                window["Like"].update('Like',button_color = "red")
                videoDislikeCount = c.execute("SELECT dislike_count FROM Video WHERE videoid = " + str(videoid) )
                videoDislikeCount = videoDislikeCount.fetchone()
                videoDislikeCount = videoDislikeCount[0]
                newVideoDislikeCount = videoDislikeCount +  1
                update = "UPDATE Video SET dislike_count = " + str(newVideoDislikeCount)+ " WHERE videoid = " + str(videoid)
                c.execute(update)
                conn.commit()
                likeEvent = c.execute("SELECT videoid FROM LikeDislike WHERE videoid = " + str(videoid) + " and user_id = " + str(in_userid)+ " and status IN  ('like','dislike')")
                likeEvent = likeEvent.fetchone()
                if not likeEvent:
                    print(17)
                    insert = "INSERT INTO LikeDislike (videoid, user_id, status) VALUES (" + str(videoid) + ", " + str(in_userid) + ", 'dislike');"
                    c.execute(insert)
                    conn.commit()
                window["dislikeCountText"].update(newVideoDislikeCount)  


            
    window.close()

def getDate(upload_date):
        today = str(date.today())
        date_format = "%Y-%m-%d"
        a = datetime.strptime(upload_date, date_format)
        b = datetime.strptime(today, date_format)
        delta = b - a
        days = delta.days
        years = days//365
        month = (days - years*365)//30
        days = days - years*365 - month*30
        if years == 0:    
            if month == 0:
                upload_info = str(days) + " days"
            else:
                upload_info = str(days) + " days, "  + str(month) + " months"
        else:
            upload_info = str(days) + " days, "  +str(month) + " months, "+ str(years) + " years"
        return upload_info

def tableVideos(typeFilter, tagFilter, state):
    if state == 200:
        videos = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id FROM Video WHERE vis=1 ")
        videos =  videos.fetchall()
    if state == 211:
        videos = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id FROM Video WHERE  vis=1 and typeid =" + str(typeFilter)+ " and videoid in (SELECT videoid FROM has_tag WHERE tag_id = " +str(tagFilter) +")")
        videos =  videos.fetchall()
    if state == 201:
        videos = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id FROM Video WHERE  vis=1 and videoid in (SELECT videoid FROM has_tag WHERE tag_id = " +str(tagFilter) +")")
        videos =  videos.fetchall()        
    if state == 210:
        videos = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id FROM Video WHERE vis=1 and typeid =" + str(typeFilter))
        videos =  videos.fetchall()

    videoList = []
    for i in range(len(videos)):
        com = "SELECT typetext FROM video_type WHERE typeid = " + str(videos[i][2])
        video_type = c.execute(com)
        video_type = video_type.fetchall()
        com2 = "SELECT uname FROM User WHERE user_id = " + str(videos[i][5])
        user = c.execute(com2)
        user = user.fetchall()
        com3 = "SELECT upload_date FROM Video_Upload WHERE videoid = " + str(videos[i][0])
        upload_date = c.execute(com3)
        upload_date = upload_date.fetchall()
        upload_date = upload_date[0][0]
        
        upload_info = getDate(upload_date)
        
        videoList.append([videos[i][0],videos[i][1],video_type[0],videos[i][3],videos[i][4],user[0][0],upload_info])

    return videoList

def windowStandard(in_userid):
    
    
    sg.theme('DarkTeal')  
    header_list = ["Video ID","Video","Type","Duration","View Count","User","Upload Date"]   
    video_table = tableVideos(0,0,200)
    getTypes  = c.execute("SELECT typeid,typetext FROM video_type")
    getTypes  =  getTypes.fetchall()
    comboType = getTypes
    
    getTag = c.execute("SELECT tag_id,tagtext FROM video_tag")
    getTag =  getTag.fetchall()
    comboTag  = getTag
    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Search a video')],
              [sg.Input( enable_events=True, key="inputSearch")],
              [sg.Text('Type'),sg.InputCombo(comboType, size=(20, 3),key="type"),sg.Text('Tag'),sg.InputCombo(comboTag,key ="tag", size=(20, 3)),sg.Button("Filter"),sg.Button("Clear")],
              [sg.Table(values=video_table,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")]]

    window = sg.Window('', layout)
    # Event Loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":             
            window.close()
            StandardLogIn()
            break
        if event == "Filter":
            if values["type"] != '': 
                if values["tag"] != '': 
                    filteredTable = tableVideos(values["type"][0], values["tag"][0], 211)
                else: 
                    filteredTable = tableVideos(values["type"][0], 0, 210)
            else:
                if values["tag"] != '': 
                    filteredTable = tableVideos(0, values["tag"][0], 201)
                else: 
                    filteredTable = tableVideos(0, 0, 200)
                    
            if values["inputSearch"] != '':                
                search = values["inputSearch"]
                new_values = []
                for i in range (len(filteredTable)):
                    if search in filteredTable[i][1]:
                        new_values.append(filteredTable[i])
                window["table"].update(new_values) 
                sVideoTable = new_values
            
            else:
                window["table"].update(filteredTable)
                sVideoTable = filteredTable

                
        else:
            if values["type"] != '' or values["tag"] != '':
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(filteredTable)):
                        if search in filteredTable[i][1]:
                            new_values.append(filteredTable[i])
                    window["table"].update(new_values)   
                    sVideoTable = new_values
                
                else:
                    window["table"].update(filteredTable)
                    sVideoTable = filteredTable
            else: 

                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(video_table)):
                        if search in video_table[i][1]:
                            new_values.append(video_table[i])
                    window["table"].update(new_values)     
                    sVideoTable = new_values
                else:
                    window["table"].update(video_table)
                    sVideoTable = video_table
        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                videoid = sVideoTable[row]
                window.close()
                videoPage(int(videoid[0]),in_userid,"Standard")
                
        if event == "Clear":
            keys_to_clear = ["inputSearch","type","tag","table"]
            for key in keys_to_clear:
                window[key]('')
                window["table"].update(video_table)  
                sVideoTable = video_table
    window.close()
    
def editdelete(videoid,in_userid):
    sg.theme('DarkTeal')
    getTag = c.execute("SELECT tag_id,tagtext FROM video_tag")
    getTag =  getTag.fetchall()
    comboTag  = getTag
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('  '*30),sg.Button('Delete',button_color = "CadetBlue")],
              [sg.Text('Edit')],
              [sg.Text('Video Name '),sg.Input(enable_events=True, key="inputName"),sg.Button('Change Name')],
              [sg.Text('Description'),sg.Input(enable_events=True,key="inputDesc"),sg.Button('Change Description')],
              [sg.Text('Tag')],
              [sg.Text('Tags'),sg.InputCombo(comboTag, size=(20, 3),key="tagAdd"),sg.Button('Add Tag')]]
    window = sg.Window('Settings', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):  
            myvideo(in_userid)             
            break
        if event == 'Back':
            myvideo(in_userid)
            break
        if event == 'Delete':
            c.execute("DELETE FROM Video WHERE videoid = " + str(videoid))
            conn.commit()
            sg.Popup("Deletion Successful!")
            myvideo(in_userid)
            break
        if event == 'Change Name':
            commandNUpdate = "UPDATE Video SET v_name = '" + str(values["inputName"] + "' WHERE videoid = " + str(videoid))
            c.execute(commandNUpdate)
            conn.commit()
        if event == 'Change Description':
            c.execute("UPDATE Video SET description = '" + str(values["inputDesc"] + "' WHERE videoid = " + str(videoid)))
            conn.commit()
        if event == 'Add Tag':
            c.execute("INSERT INTO has_tag (tag_id,videoid)  VALUES ("+str(values["tagAdd"][0])+","+str(videoid)+")")
            conn.commit()
    window.close()

def createVideo (in_userid):
    sg.theme('DarkTeal')
    getTypes  = c.execute("SELECT typeid,typetext FROM video_type")
    getTypes  =  getTypes.fetchall()
    comboType = getTypes
    
    getPref  = c.execute("SELECT pref_type_id,pref_type FROM Pref_type")
    getPref  =  getPref.fetchall()
    comboPref = getPref
    numVideo = c.execute("SELECT videoid FROM Video ")
    numVideo = numVideo.fetchall()
    num = len(numVideo)
    videoid = 150 + num
    user = in_userid
    ads_id = "NULL" 
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('New Video')],
              [sg.Text('Video Name'),sg.Input(enable_events=True, key="videoName")],
              [sg.Text('Description'),sg.Input(enable_events=True, key="videoDesc")],
              [sg.Text('Duration'),sg.Input(enable_events=True, key="videoDuration")],
              [sg.Text('Video Type'),sg.InputCombo(comboType, size=(20, 3),key="videoType")],
              [sg.Text('Advertisement Type'),sg.InputCombo(comboPref, size=(20, 3),key="videoPref")],
              [sg.Button('Publish Video')]]
    
    window = sg.Window('', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Back', 'Exit'):  
            window.close()
            myvideo(in_userid)             
            break
        if event == "Publish Video":
            videoPublishCommand = "INSERT INTO Video (videoid,duration,v_name,description,like_count,dislike_count,view_count,ads_id,user_id,pref_type_id,typeid,vis) VALUES (" + str(videoid) + ',' + str(values["videoDuration"]) + ',' + "'" + str(values["videoName"]) + "'" + ',' + "'" + str(values["videoDesc"]) + "'" + ',0,0,0,' + str(ads_id) + ','  + str(user) + ',' +  str(values["videoPref"][0]) + ',' +  str(values["videoType"][0]) + ',' + "FALSE" + ')'
            c.execute(videoPublishCommand)
            up_date = date.today()
            up_date = str(up_date)
            video_IP = 21902
            videoUploadCommand = "INSERT INTO Video_upload (user_id,videoid,upload_date,video_IP) VALUES (" + str(user) + ','  + str(videoid) + ','  + "'"+ str(up_date) +  "'"+',' + "'"+ str(video_IP) +  "'" + ')'
            c.execute(videoUploadCommand)
            conn.commit()
            print("Executed!")
            sg.Popup("Video is published successfully! Waiting for admin approval! ")
            myvideo(in_userid)
            break
    window.close()
    
def myvideo(in_userid):
    sg.theme('DarkTeal')   
    header_list = ["Video ID","Video Name","Description","Like","Dislike","View Count","Visibility"]   
    videos = c.execute("SELECT videoid,v_name,description,like_count,dislike_count,view_count,vis FROM Video WHERE user_id = " + str(in_userid))
    videos =  videos.fetchall()

    videotab = []
    for i in range(len(videos)):
        videotab.append([videos[i][0],videos[i][1],videos[i][2],videos[i][3],videos[i][4],videos[i][5],videos[i][6]])
        
    layout = [[sg.Text('My Videos')],
              [sg.Button('Back'),sg.Button('Exit')],
              [sg.Table(values=videotab,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")],
              [sg.Button('Create New Video')]]
    window1 = sg.Window('My Videos', layout)
    
    while True:
        event, values = window1.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                
            break
        if event == 'Back':
            window1.close()
            windowPartner(in_userid)
            break
        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                videoid = videotab[row][0]
                editdelete(videoid,in_userid)
                break
        if event == "Create New Video":
            window1.close()
            createVideo(in_userid)
            break
        
    window1.close()

def windowPartner(in_userid):
    sg.theme('DarkTeal')  
    header_list = ["Video ID","Video","Type","Duration","View Count","User","Upload Date"]   
    video_table = tableVideos(0,0,200)
    getTypes  = c.execute("SELECT typeid,typetext FROM video_type")
    getTypes  =  getTypes.fetchall()
    comboType = getTypes
    
    getTag = c.execute("SELECT tag_id,tagtext FROM video_tag")
    getTag =  getTag.fetchall()
    comboTag  = getTag
    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Search a video')],
              [sg.Input( enable_events=True, key="inputSearch")],
              [sg.Text('Type'),sg.InputCombo(comboType, size=(20, 3),key="type"),sg.Text('Tag'),sg.InputCombo(comboTag,key ="tag", size=(20, 3)),sg.Button("Filter"),sg.Button("Clear")],
              [sg.Table(values=video_table,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")],
              [sg.Button('My Videos'),sg.Button('My Payments')]]

    window = sg.Window('', layout)
    # Event Loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":             
            window.close()
            PartnerLogIn()
            break
        if event == "My Videos":             
            myvideo(in_userid)
            break
        if event == "My Payments":             
            prevPayments(in_userid)

        if event == "Filter":
            if values["type"] != '': 
                if values["tag"] != '': 
                    filteredTable = tableVideos(values["type"][0], values["tag"][0], 211)
                else: 
                    filteredTable = tableVideos(values["type"][0], 0, 210)
            else:
                if values["tag"] != '': 
                    filteredTable = tableVideos(0, values["tag"][0], 201)
                else: 
                    filteredTable = tableVideos(0, 0, 200)
                    
            if values["inputSearch"] != '':                
                search = values["inputSearch"]
                new_values = []
                for i in range (len(filteredTable)):
                    if search in filteredTable[i][1]:
                        new_values.append(filteredTable[i])
                window["table"].update(new_values) 
                sVideoTable = new_values
            
            else:
                window["table"].update(filteredTable)
                sVideoTable = filteredTable

                
        else:
            if values["type"] != '' or values["tag"] != '':
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(filteredTable)):
                        if search in filteredTable[i][1]:
                            new_values.append(filteredTable[i])
                    window["table"].update(new_values)   
                    sVideoTable = new_values
                
                else:
                    window["table"].update(filteredTable)
                    sVideoTable = filteredTable
            else: 

                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(video_table)):
                        if search in video_table[i][1]:
                            new_values.append(video_table[i])
                    window["table"].update(new_values)     
                    sVideoTable = new_values
                else:
                    window["table"].update(video_table)
                    sVideoTable = video_table
        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                videoid = sVideoTable[row]
                window.close()
                videoPage(int(videoid[0]),in_userid,"Partner")
                
        if event == "Clear":
            keys_to_clear = ["inputSearch","type","tag","table"]
            for key in keys_to_clear:
                window[key]('')
                window["table"].update(video_table)  
                sVideoTable = video_table
    window.close()     

def StandardLogIn():
    sg.theme('DarkTeal')   
    layout = [  [sg.Text('Welcome!')],
                [sg.Text('Username'), sg.InputText(key="username")],
                [sg.Text('Password'), sg.InputText(key="password")],
                [sg.Button('Log In'), sg.Button('Back'),sg.Button('Exit')] ] 
    window = sg.Window('Standard User', layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                
            break
        if event == 'Back':
            window.close()
            EntryPage()
            break
        
        in_userid = values["username"]
        in_password = values["password"]
       
        try:
            comStandard = "SELECT user_id FROM Standard WHERE user_id = " + str(in_userid)
            ifStandard = c.execute(comStandard)
            ifStandard = ifStandard.fetchall()
            if ifStandard:
                comPassword = "SELECT password FROM User WHERE user_id = " + str(in_userid)   
                comPassword = c.execute(comPassword)
                comPassword = comPassword.fetchone()
                if comPassword is not None:
                    if comPassword[0] == in_password:
                        window.close()
                        windowStandard(in_userid)
                        break
                    else:
                        sg.Popup('Invalid username or password!')
                
                else:
                    sg.Popup('Invalid username or password!')
            else:
                sg.Popup('Invalid username or password!')
        except:
            sg.Popup('Sorry, please try again!')
    
    window.close()

def PartnerLogIn():
    sg.theme('DarkTeal')   
    layout = [  [sg.Text('Welcome!')],
                [sg.Text('Username'), sg.InputText(key="username")],
                [sg.Text('Password'), sg.InputText(key="password")],
                [sg.Button('Log In'), sg.Button('Back'),sg.Button('Exit')] ] 
    window = sg.Window('Partner User', layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                
            break
        if event == 'Back':
            window.close()
            EntryPage()
            break
        
        in_userid = values["username"]
        in_password = values["password"]
       
        try:
            comStandard = "SELECT user_id FROM Partner WHERE user_id = " + str(in_userid)
            ifStandard = c.execute(comStandard)
            ifStandard = ifStandard.fetchall()
            if ifStandard:
                comPassword = "SELECT password FROM User WHERE user_id = " + str(in_userid)   
                comPassword = c.execute(comPassword)
                comPassword = comPassword.fetchone()
                if comPassword is not None:
                    if comPassword[0] == in_password:
                        window.close()
                        windowPartner(in_userid)
                        break
                    else:
                        sg.Popup('Invalid username or password!')
                
                else:
                    sg.Popup('Invalid username or password!')
            else:
                sg.Popup('Invalid username or password!')
        except:
            sg.Popup('Sorry, please try again!')
    
    window.close()
def adsDetailPage(in_userid,pref_id,videoID):
    sg.theme('DarkTeal')  
    header_list = ["Advertisement ID","Advertisement Name","Content","Flag","Company"]   
    videos = c.execute("SELECT ads_id,a_name,content,flags FROM Ads WHERE pref_type_id=" + str(pref_id))
    videos =  videos.fetchall()
    video_table = []
    for i in range(len(videos)): 
        compID = c.execute("SELECT compid FROM has_ads WHERE ads_id =" + str(videos[i][0]))
        compID = compID.fetchall()
        compName = c.execute("SELECT cname FROM Company WHERE compid =" + str(compID[i][0]))
        compName = compName.fetchall()
        compName = compName[0]
        video_table.append([videos[i][0],videos[i][1],videos[i][2],videos[i][3],compName])

    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Advertisement Information')],
              [sg.Table(values=video_table,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")]]

    window = sg.Window('', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":         
            window.close()
            windowAdmin(in_userid)
            break

        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                ads = video_table[row]
                adsID = str(ads[0])
                print(adsID)
                print(type(adsID))
                print(videoID)
                print(type(videoID))
                adsIDUpdate = "UPDATE Video SET ads_id =" + adsID  +  " WHERE videoid =" + str(videoID)
                c.execute(adsIDUpdate)
                conn.commit()
                nonAdsVideo(in_userid)
                break
            
    window.close()    
    
def nonAdsVideo(in_userid):
    sg.theme('DarkTeal')  
    header_list = ["Video ID","Video","Type","Duration","View Count","User","Upload Date"]   
    videos = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id FROM Video WHERE ads_id IS NULL")
    videos =  videos.fetchall()
    video_table = []
    for i in range(len(videos)):
        com = "SELECT typetext FROM video_type WHERE typeid = " + str(videos[i][2])
        video_type = c.execute(com)
        video_type = video_type.fetchall()
        com2 = "SELECT uname FROM User WHERE user_id = " + str(videos[i][5])
        user = c.execute(com2)
        user = user.fetchall()
        com3 = "SELECT upload_date FROM Video_Upload WHERE videoid = " + str(videos[i][0])
        upload_date = c.execute(com3)
        upload_date = upload_date.fetchall()
        upload_date = upload_date[0][0]
        
        upload_info = getDate(upload_date)
        
        video_table.append([videos[i][0],videos[i][1],video_type[0],videos[i][3],videos[i][4],user[0][0],upload_info])

    getTypes  = c.execute("SELECT typeid,typetext FROM video_type")
    getTypes  =  getTypes.fetchall()
    comboType = getTypes
    
    getTag = c.execute("SELECT tag_id,tagtext FROM video_tag")
    getTag =  getTag.fetchall()
    comboTag  = getTag
    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Non-Ads Videos')],
              [sg.Text('Search a video')],
              [sg.Input( enable_events=True, key="inputSearch")],
              [sg.Text('Type'),sg.InputCombo(comboType, size=(20, 3),key="type"),sg.Text('Tag'),sg.InputCombo(comboTag,key ="tag", size=(20, 3)),sg.Button("Filter"),sg.Button("Clear")],
              [sg.Table(values=video_table,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")]]

    window = sg.Window('', layout)
    # Event Loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":         
            window.close()
            windowAdmin(in_userid)
            break

        
        if event == "Filter":
            if values["type"] != '': 
                if values["tag"] != '': 
                    filteredTable = tableVideos(values["type"][0], values["tag"][0], 211)
                else: 
                    filteredTable = tableVideos(values["type"][0], 0, 210)
            else:
                if values["tag"] != '': 
                    filteredTable = tableVideos(0, values["tag"][0], 201)
                else: 
                    filteredTable = tableVideos(0, 0, 200)
                    
            if values["inputSearch"] != '':                
                search = values["inputSearch"]
                new_values = []
                for i in range (len(filteredTable)):
                    if search in filteredTable[i][1]:
                        new_values.append(filteredTable[i])
                window["table"].update(new_values) 
                sVideoTable = new_values
            
            else:
                window["table"].update(filteredTable)
                sVideoTable = filteredTable

                
        else:
            if values["type"] != '' or values["tag"] != '':
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(filteredTable)):
                        if search in filteredTable[i][1]:
                            new_values.append(filteredTable[i])
                    window["table"].update(new_values)   
                    sVideoTable = new_values
                
                else:
                    window["table"].update(filteredTable)
                    sVideoTable = filteredTable
            else: 
                
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(video_table)):
                        if search in video_table[i][1]:
                            new_values.append(video_table[i])
                    window["table"].update(new_values)     
                    sVideoTable = new_values
                else:
                    window["table"].update(video_table)
                    sVideoTable = video_table
        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                videoid = sVideoTable[row]
                prefferedCommand = "SELECT pref_type_id FROM Video WHERE videoid = " + str(int(videoid[0]))
                prefferedAds = c.execute(prefferedCommand)
                prefferedAds = prefferedAds.fetchone()
                prefferedAds = prefferedAds[0]
                window.close()
                adsDetailPage(in_userid,prefferedAds,str(int(videoid[0])))
                
        if event == "Clear":
            keys_to_clear = ["inputSearch","type","tag","table"]
            for key in keys_to_clear:
                window[key]('')
                window["table"].update(video_table)  
                sVideoTable = video_table
    window.close() 
def reviewVideo(in_userid):
    sg.theme('DarkTeal')  
    header_list = ["Video ID","Video","Type","Duration","View Count","User","Upload Date"]   
    videos = c.execute("SELECT videoid,v_name,typeid,duration,view_count,user_id FROM Video WHERE vis!=1 ")
    videos =  videos.fetchall()
    video_table = []
    for i in range(len(videos)):
        com = "SELECT typetext FROM video_type WHERE typeid = " + str(videos[i][2])
        video_type = c.execute(com)
        video_type = video_type.fetchall()
        com2 = "SELECT uname FROM User WHERE user_id = " + str(videos[i][5])
        user = c.execute(com2)
        user = user.fetchall()
        com3 = "SELECT upload_date FROM Video_Upload WHERE videoid = " + str(videos[i][0])
        upload_date = c.execute(com3)
        upload_date = upload_date.fetchall()
        upload_date = upload_date[0][0]
        
        upload_info = getDate(upload_date)
        
        video_table.append([videos[i][0],videos[i][1],video_type[0],videos[i][3],videos[i][4],user[0][0],upload_info])

    getTypes  = c.execute("SELECT typeid,typetext FROM video_type")
    getTypes  =  getTypes.fetchall()
    comboType = getTypes
    
    getTag = c.execute("SELECT tag_id,tagtext FROM video_tag")
    getTag =  getTag.fetchall()
    comboTag  = getTag
    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Approve Videos')],
              [sg.Text('Search a video')],
              [sg.Input( enable_events=True, key="inputSearch")],
              [sg.Text('Type'),sg.InputCombo(comboType, size=(20, 3),key="type"),sg.Text('Tag'),sg.InputCombo(comboTag,key ="tag", size=(20, 3)),sg.Button("Filter"),sg.Button("Clear")],
              [sg.Table(values=video_table,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")]]

    window = sg.Window('', layout)
    # Event Loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":         
            window.close()
            windowAdmin(in_userid)
            break

        
        if event == "Filter":
            if values["type"] != '': 
                if values["tag"] != '': 
                    filteredTable = tableVideos(values["type"][0], values["tag"][0], 211)
                else: 
                    filteredTable = tableVideos(values["type"][0], 0, 210)
            else:
                if values["tag"] != '': 
                    filteredTable = tableVideos(0, values["tag"][0], 201)
                else: 
                    filteredTable = tableVideos(0, 0, 200)
                    
            if values["inputSearch"] != '':                
                search = values["inputSearch"]
                new_values = []
                for i in range (len(filteredTable)):
                    if search in filteredTable[i][1]:
                        new_values.append(filteredTable[i])
                window["table"].update(new_values) 
                sVideoTable = new_values
            
            else:
                window["table"].update(filteredTable)
                sVideoTable = filteredTable

                
        else:
            if values["type"] != '' or values["tag"] != '':
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(filteredTable)):
                        if search in filteredTable[i][1]:
                            new_values.append(filteredTable[i])
                    window["table"].update(new_values)   
                    sVideoTable = new_values
                
                else:
                    window["table"].update(filteredTable)
                    sVideoTable = filteredTable
            else: 
                
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(video_table)):
                        if search in video_table[i][1]:
                            new_values.append(video_table[i])
                    window["table"].update(new_values)     
                    sVideoTable = new_values
                else:
                    window["table"].update(video_table)
                    sVideoTable = video_table
        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                videoid = sVideoTable[row]
                visCommand = "UPDATE Video SET vis = 1 WHERE videoid = " + str(int(videoid[0]))
                c.execute(visCommand)
                conn.commit()
                window.close()
                sg.Popup("Video is visible for everyone!")
                reviewVideo(in_userid)
                
                
        if event == "Clear":
            keys_to_clear = ["inputSearch","type","tag","table"]
            for key in keys_to_clear:
                window[key]('')
                window["table"].update(video_table)  
                sVideoTable = video_table
    window.close() 
def companyAdsDetails(ads):
    sg.theme('DarkTeal')  
    cheader_list = ["Ads ID","Ads Name"]   
    comp_table = []
    for i in range(len(ads)):
        comp_table.append([ads[i][0],ads[i][1]])
   
    layout = [[sg.Button('Back'),
              [sg.Text('Ads Information')],
              [sg.Table(values=comp_table,
                  headings=cheader_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="adsTable")]]]
    window = sg.Window('Company & Partner Information', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Back'):             
            break               
    window.close()
    
def prevPayments(partnerID):
    sg.theme('DarkTeal')  
    cheader_list = ["Transaction ID","Amount"]   
    prev = c.execute("SELECT transactionid,amount FROM Receive WHERE user_id = " + str(partnerID))
    previous = prev.fetchall()
    comp_table = []
    for i in range(len(previous)):
        comp_table.append([previous[i][0],previous[i][1]])
   
    layout = [[sg.Button('Back'),
              [sg.Text('Previous Payments')],
              [sg.Table(values=comp_table,
                  headings=cheader_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="prevTable")]]]
    window = sg.Window('Company & Partner Information', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Back'):             
            break               
    window.close()
    
def partnerAdsDetails(partnerID,partnerAdsDet,in_userid):
    sg.theme('DarkTeal')  
    cheader_list = ["Video Name","Company Name","Ads ID","Ads Name"]   
    comp_table = []
    for i in range(len(partnerAdsDet)):
        comp_table.append([partnerAdsDet[i][0],partnerAdsDet[i][1],partnerAdsDet[i][2],partnerAdsDet[i][3]])
    layout = [[sg.Button('Back')],
              [sg.Text('Partner Ads Information')],
              [sg.Table(values=comp_table,
                  headings=cheader_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="adsTable")],
              [sg.Button('Make Payments',button_color = "green4"),sg.Button('Previous Payments',button_color = "NavajoWhite4")]]
    window = sg.Window('Company & Partner Information', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Back'):             
            break   
        
        if event == "Make Payments":     
            transactionid = randint(100000, 999999)
            amount = randint(100, 2500)
            co = "INSERT INTO Receive (user_id,transactionid,amount) VALUES (" + str(partnerID) + ", " + str(transactionid) + "," +str(amount)+")"
            c.execute(co)
            conn.commit()
            sg.Popup("Payment successful!")
        
        if event == "Previous Payments":         
            prevPayments(partnerID)
    window.close()
    
def paymentAdmin(in_userid):
    sg.theme('DarkTeal')  
    cheader_list = ["Company ID","Company Name","Company IBAN"]   
    companies = c.execute("SELECT compid,cname,IBAN2 FROM Company ")
    companies =  companies.fetchall()
    comp_table = []
    for i in range(len(companies)):
        comp_table.append([companies[i][0],companies[i][1],companies[i][2]])
   
    pheader_list = ["Partner ID","Partner Name","Partner IBAN"]   
    partners = c.execute("SELECT U.user_id,U.uname,P.IBAN2 FROM User U, Partner P WHERE P.user_id =U.user_id ")
    partners =  partners.fetchall()
    partner_table = []
    for i in range(len(partners)):
        partner_table.append([partners[i][0],partners[i][1],partners[i][2]])
    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Company Information')],
              [sg.Table(values=comp_table,
                  headings=cheader_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="companyTable")],
              [sg.Text('Partner Information')],
              [sg.Table(values=partner_table,
                  headings=pheader_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="partnerTable")]]
    
    window = sg.Window('Company & Partner Information', layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":         
            window.close()
            windowAdmin(in_userid)
            break
        if event == "companyTable":         
            if len(values['companyTable']) > 0:
                row = values[event][0]
                compID = comp_table[row]
                compID = compID[0]
                compAdsCommand = "SELECT A.ads_id, A.a_name FROM has_ads H, Ads A WHERE H.ads_id =  A.ads_id and H.compid = " + str(compID)
                t = c.execute(compAdsCommand)
                t = t.fetchall()
                companyAdsDetails(t)
                
        if event == "partnerTable":         
            if len(values['partnerTable']) > 0:
                row = values[event][0]
                partnerID = partner_table[row]
                partnerID = partnerID[0]
                partnerAdsCommand = "SELECT V.v_name, C.cname,H.ads_id,A.a_name FROM Video V, has_ads H, Company C,Ads A WHERE V.ads_id = H.ads_id and H.compid =  C.compid and H.ads_id = A.ads_id and V.user_id = " + str(partnerID)
                y = c.execute(partnerAdsCommand)
                y = y.fetchall()
                partnerAdsDetails(partnerID,y,in_userid)
                
    window.close()
    
def windowAdmin(in_userid):
    sg.theme('DarkTeal')  
    header_list = ["Video ID","Video","Type","Duration","View Count","User","Upload Date"]   
    video_table = tableVideos(0,0,200)
    getTypes  = c.execute("SELECT typeid,typetext FROM video_type")
    getTypes  =  getTypes.fetchall()
    comboType = getTypes
    
    getTag = c.execute("SELECT tag_id,tagtext FROM video_tag")
    getTag =  getTag.fetchall()
    comboTag  = getTag
    
    layout = [[sg.Button('Back'),sg.Button('Exit')],
              [sg.Text('Search a video')],
              [sg.Input( enable_events=True, key="inputSearch")],
              [sg.Text('Type'),sg.InputCombo(comboType, size=(20, 3),key="type"),sg.Text('Tag'),sg.InputCombo(comboTag,key ="tag", size=(20, 3)),sg.Button("Filter"),sg.Button("Clear"),sg.Button("Review",button_color = "DeepSkyBlue2"),sg.Button("Non-Ads Videos",button_color = "MediumPurple1")],
              [sg.Table(values=video_table,
                  headings=header_list,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  enable_events=True,
                  key="table")],
              [sg.Button('Payment Page',button_color = 'ForestGreen')]]

    window2 = sg.Window('', layout)
    # Event Loop
    while True:
        event, values = window2.read()
        if event in (sg.WIN_CLOSED,'Exit'):             
            break
        if event == "Back":             
            window2.close()
            AdminLogIn()
            break
        if event == "Non-Ads Videos": 
            window2.close()
            nonAdsVideo(in_userid)
            break
        if event == "Review": 
            window2.close()
            reviewVideo(in_userid)
            break
        
        if event == "Payment Page": 
            window2.close()
            paymentAdmin(in_userid)
            break
        
        if event == "Filter":
            if values["type"] != '': 
                if values["tag"] != '': 
                    filteredTable = tableVideos(values["type"][0], values["tag"][0], 211)
                else: 
                    filteredTable = tableVideos(values["type"][0], 0, 210)
            else:
                if values["tag"] != '': 
                    filteredTable = tableVideos(0, values["tag"][0], 201)
                else: 
                    filteredTable = tableVideos(0, 0, 200)
                    
            if values["inputSearch"] != '':                
                search = values["inputSearch"]
                new_values = []
                for i in range (len(filteredTable)):
                    if search in filteredTable[i][1]:
                        new_values.append(filteredTable[i])
                window2["table"].update(new_values) 
                sVideoTable = new_values
            
            else:
                window2["table"].update(filteredTable)
                sVideoTable = filteredTable

                
        else:
            if values["type"] != '' or values["tag"] != '':
                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(filteredTable)):
                        if search in filteredTable[i][1]:
                            new_values.append(filteredTable[i])
                    window2["table"].update(new_values)   
                    sVideoTable = new_values
                
                else:
                    window2["table"].update(filteredTable)
                    sVideoTable = filteredTable
            else: 

                if values["inputSearch"] != '':                
                    search = values["inputSearch"]
                    new_values = []
                    for i in range (len(video_table)):
                        if search in video_table[i][1]:
                            new_values.append(video_table[i])
                    window2["table"].update(new_values)     
                    sVideoTable = new_values
                else:
                    window2["table"].update(video_table)
                    sVideoTable = video_table
        if event == "table":
            if len(values['table']) > 0:
                row = values[event][0]
                videoid = sVideoTable[row]
                window2.close()
                videoPage(int(videoid[0]),in_userid,"Partner")
                
        if event == "Clear":
            keys_to_clear = ["inputSearch","type","tag","table"]
            for key in keys_to_clear:
                window2[key]('')
                window2["table"].update(video_table)  
                sVideoTable = video_table
    window2.close() 
    
def AdminLogIn():
    sg.theme('DarkTeal')   
    layout = [  [sg.Text('Welcome!')],
                [sg.Text('Username'), sg.InputText(key="username")],
                [sg.Text('Password'), sg.InputText(key="password")],
                [sg.Button('Log In'), sg.Button('Back'),sg.Button('Exit')] ] 
    window = sg.Window('Admin User', layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                
            break
        if event == 'Back':
            window.close()
            EntryPage()
            break
        
        in_userid = values["username"]
        in_password = values["password"]
       
        try:
            comStandard = "SELECT user_id FROM Admin WHERE user_id = " + str(in_userid)
            ifStandard = c.execute(comStandard)
            ifStandard = ifStandard.fetchall()
            if ifStandard:
                comPassword = "SELECT password FROM User WHERE user_id = " + str(in_userid)   
                comPassword = c.execute(comPassword)
                comPassword = comPassword.fetchone()
                if comPassword is not None:
                    if comPassword[0] == in_password:
                        window.close()
                        windowAdmin(in_userid)
                        break
                    else:
                        sg.Popup('Invalid username or password!')
                else:
                    sg.Popup('Invalid username or password!')
            else:
                sg.Popup('Invalid username or password!')
        except:
            sg.Popup('Sorry, please try again!')
    
    window.close()

def EntryPage():
    sg.theme('DarkTeal')   
    layout = [[sg.Button("Standard",key="standard"), sg.Button("Partner",key="partner"),sg.Button("Admin",key="admin")]] 
    window = sg.Window('Video Sharing Platform', layout,size=(290, 50))
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                
            break
        if event  =="standard":
            window.close()
            StandardLogIn()
        if event  =="partner":
            window.close()
            PartnerLogIn()
        if event  =="admin":
            window.close()
            AdminLogIn()
EntryPage()
conn.close()