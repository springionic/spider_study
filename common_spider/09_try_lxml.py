from lxml import etree

text = '''
  <div class="nav_wrap " id="tb_nav">
        <ul class="nav_list j_nav_list">
                                <li class=" focus j_tbnav_tab " data-tab-main>
    <a  class="j_nav_local_tab_link j_tbnav_tab_a" id="tab_forumname" stats-data="fr=tb0_forum&st_mod=frs&st_value=tabmain">看贴_1</a>
</li>                                <li class=" j_tbnav_tab " data-tab-album>
    <a href="href_2" class="j_nav_local_tab_link j_tbnav_tab_a" stats-data="fr=tb0_forum&st_mod=frs&st_value=tabfrsphotogood" frs-page="main" id="tab_picture">图片_2</a>
</li>                                <li class=" j_tbnav_tab " data-tab-good>
    <a href="href_3" class="j_nav_local_tab_link j_tbnav_tab_a" stats-data="fr=tb0_forum&st_mod=frs&st_value=tabgood">精品_3</a>
</li>                                <li class=" j_tbnav_tab " data-tab-video>
    <a href="href_4" class="j_nav_local_tab_link j_tbnav_tab_a" stats-data="fr=tb0_forum&st_mod=frs&st_value=tabvideo">视频_4</a>
</li>                            </ul>
                            <form class="search_internal_wrap pull_right j_search_internal_forum">
                <input class="search_internal_input j_search_internal_input" value="" placeholder="吧内搜索" type="text"/>
                <button class="search_internal_btn" type="submit"/>
                <i></i></button>
            </form>
            </div>

'''
html = etree.HTML(text)
print(html)
# 查询#lement对象中包含的字符串
print(etree.tostring(html).decode())

# 获取
res = html.xpath(r'//li/a[@class="j_nav_local_tab_link j_tbnav_tab_a"]/@href')
print(res)
res2 = html.xpath(r'//li/a[@class="j_nav_local_tab_link j_tbnav_tab_a"]/text()')
print(res2)
# 每个li是一条新闻，把url和文本组成字典
for href in res:
    item = {}
    item['href'] = href
    item['title'] = res2[res.index(href)]
    print(item)
print('*' * 180)
# 分组，根据a标签进行分组，对每一组继续写xpath
res3 = html.xpath(r'//li/a[@class="j_nav_local_tab_link j_tbnav_tab_a"]')
print(res3)
for i in res3:
    item = {}
    item['title'] = i.xpath('./text()')[0] if len(i.xpath('./text()')) else None
    item['href'] = i.xpath('./@href')[0] if len(i.xpath('./@href')) else None
    print(item)
