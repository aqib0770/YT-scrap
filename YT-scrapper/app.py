from flask import Flask,render_template
from flask_cors import CORS,cross_origin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
app=Flask(__name__,template_folder='template')
@cross_origin
@app.route('/')
def scrap():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/@PW-Foundation/videos')
    body=driver.find_element(By.TAG_NAME,'body')
    for i in range(7):
        body.send_keys(Keys.PAGE_DOWN)
    video_links=driver.find_elements(By.CSS_SELECTOR,'a[href*="/watch?v="]')
    video_title=driver.find_elements(By.CSS_SELECTOR,'a[id*="video-title-link"]')
    thumbnail_elements = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]//yt-image//img')
    video_views=driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[1]')
    video_time = driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[2]')

    links=[]
    titles=[]
    views=[]
    time=[]
    thumbnails=[]
    for i in range(5):
        #extracting links
        href=video_links[i].get_attribute('href')
        links.append(href)
    for i in range(5):
        #extracting titles
        id=video_title[i].get_attribute('title')
        titles.append(id)
    for i in range(5):
        #extracting views
        view=video_views[i].text
        if 'views' in view:
            views.append(view)
        #extracting time
    for i in range(5):
        times=video_time[i].text
        if 'ago' in times:
            time.append(times)
    for i in range(5):
        src=thumbnail_elements[i].get_attribute('src')
        thumbnails.append(src)
        
    driver.quit()

    main_list=[]
    for i,j,k,l,m in zip(titles,links,thumbnails,views,time):
        mydict={"title":i,"links":j,"thumbnails":k,"views":l,"time":m}
        main_list.append(mydict)
    

    with open('youtube_data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Thumbnail', 'Views', 'Time'])
        for i, j, k, l, m in zip(titles, links, thumbnails, views, time):
            writer.writerow([i, j, k, l, m])


    return render_template('result.html',main_list=main_list)
if __name__=='__main__':
    app.run(host="0.0.0.0")
