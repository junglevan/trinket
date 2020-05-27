import re
from random import randint
import pandas as pd
import requests
from queue import Queue
from urllib import parse
import time
from fake_useragent import UserAgent


class Ingredient_Spider:
    def __init__(self):
        self.n = 0
        self.keyword = ''
        self.one_url = 'http://www.aiqilian.com/cid/so?wd={}'
        self.two_url = 'http://www.aiqilian.com{}'
        # 创建2个队列
        self.one_q = Queue()
        self.two_q = Queue()
        self.headers = {'User-Agent': UserAgent().random}
        # 存入json文件
        self.ingredient_info_list = [['成分', '特性', '功效', '属性', '物质']]
        # 计数
        self.i = 0
        self.ingredients_material_list = self.getlist()

    # 一级页面URL入队列
    def url_in(self):
        # 中文编码
        keyword = parse.quote(self.keyword)
        # 获取某个职位类别的总页数
        one_url = self.one_url.format(keyword)
        self.one_q.put((keyword, one_url))

    def parse_one_page(self):
        if not self.one_q.empty():
            self.i += 1
            print(self.i, 'first start')
            one_url = self.one_q.get()
            key_word = one_url[0]
            one_url = one_url[1]
            time.sleep(randint(10, 20) * 0.1)
            one_html = requests.get(url=one_url, headers=self.headers).text
            with open('one_page.html', 'w+') as f:
                f.write(one_html)
                f.seek(0)
                one_html = f.read()
            pattern = re.compile(
                '''<!--产品列表-->\n\t\t\t<div class="i_list">            \n            \t<ul>\n\t\t\t\t\n                    <li>\n                        <a href="(.+)" title=''')

            two_url = pattern.findall(one_html)
            if two_url:
                two_url = self.two_url.format(two_url[0])
                # 把详情页链接put到二级队列中
                self.two_q.put((key_word, two_url))

    # 二级页面线程事件函数:提取职位具体信息
    def parse_two_page(self):

        try:
            # 二级页面get()地址必须添加timeout参数
            two_url = self.two_q.get(block=True, timeout=3)
            self.n += 1
            print(self.n, 'second start')
            key_word = two_url[0]
            key_word = parse.unquote(key_word)
            two_url = two_url[1]
            time.sleep(randint(10, 20) * 0.1)
            two_html = requests.get(url=two_url, headers=self.headers).text
            # two_html = json.loads(requests.get(url=two_url,headers=self.headers).text) 差不多
            with open('two_page.html' , 'w+') as f:
                f.write(two_html)
                f.seek(0)
                two_html = f.read()
            pattern = re.compile(
                '''<div class="c_main_h2"><h2><i class="iconfont icon-i63"></i>成分统计</h2><a href="#"><i class="iconfont icon-i69"> Top</i></a></div>\n                <div class="c_main_dl"><dl style="width:806px;"><dt>特性</dt><dd>​(\w+)</dd></dl><dl style="width:806px;"><dt>功效</dt><dd>​(\w+)</dd></dl><dl style="width:806px;"><dt>属性</dt><dd>​(\w+)</dd></dl><dl style="width:806px;"><dt>物质</dt><dd>​(\w+)</dd></dl>''',
                re.S)
            item = pattern.findall(two_html)[0]
            print([key_word] + list(item))
            self.ingredient_info_list.append([key_word] + list(item))
            print(self.ingredient_info_list)
        except Exception as e:
            print('2',e)


    # 入口函数
    def run(self):
        # 1.URL入队列
        try:
            for keys in self.ingredients_material_list:
                self.keyword = keys
                self.url_in()
                print('keys in',self.keyword)
                self.parse_one_page()
                self.parse_two_page()
        except Exception as e:
            print(e)
        finally:
            ingredient_df = pd.DataFrame(self.ingredient_info_list)
            ingredient_df.to_csv('test.csv')
            print('数量:', self.i)


    def getlist(self):
        ingredient = '''水、甘油、PEG/PPG/聚丁二醇-8/5/3甘油、丁二醇、双丙甘醇、12-二醇、海藻糖、烟酰胺双-PEG-18甲基醚二甲基硅烷、氢化卵磷脂泛醇、蔗糖硬脂酸酯、羟脯氨酸、甜菜碱、甘油聚甲基丙烯酸酯、聚二甲基硅氧烷、鲸蜡硬脂醇、丙烯酸(酯)类/C10-30烷醇丙烯酸酯交联聚合、胆淄醇、氨丁三醇、神经酰胺3、丙二醇、香柠檬(CIRUS BERGAMIA)果油、透明质酸钠、羟乙基纤维素、亚油酸、棕榈酸、柚(CITRUS GRANDIS)果皮油、突厥蔷薇(ROSA DAMASCENA)花油、EDTA三钠、阿拉伯胶树(ACACIA SENEGSL)胶、黄花蒿(ARTEMISIA ANNUA)提取物、印度楝(AZADIRACHTA INDICA)叶提取物、B-葡聚糖、茶( SINENSIS)叶提取物、覆盆子(RUBUS IDAEUS)果提取物、 RDAMOMUM)籽油、塔希提香草兰(VANILLA TAHITENSIS)果提取物、卡波姆、辛酸/酸甘油三酯、聚山醇酯-20、酵母菌/葡萄发酵产物提取物、乳酸杆NICA)根发酵产物提取物、丁香(EUGENIA CARYOPHYLLUS)花提取物、酵母发酵产物提取物、乳酸杆菌/石榴(PUNICA GRANATUM)果发酵产物取物、醋、八角茴香(ILLICIUM VERUM)果提取物、贯叶连翘(HYPERICUM PERFORATUM)花/叶/茎提取物、茴香(FOENICULUM VULGARE)果提取物、柠檬香茅(CYMBOPOGON CITRATUS EXCELSIOR)叶提取物、欧芹(CARUM PETROSELINUM)提取物、欧夏至草(MARRUBIUM VULGARE)、欧洲白蜡树(FRAXINUS EXCELSIOR)、薰衣草花提取物(LAVANDULA ANGUSTIFOLIA INALS)、芫荽(CPRIANDRUM SATIVUM)果叶提取物、栽培黑种草(NIGELLA SATIVA)籽提取物树、姜(ZINGIBER OFFICINALE)根提取物、药鼠尾草(SALVIA OFFICINALIS)叶提取物、蜂蜜提取物、锡兰肉桂(CINNAMOMUM ZEYLANICUM)树皮提取物、缬草(VALERIANA SATIVA)根/茎根提取物、葡萄酒提取物、齿叶乳香(BOSWELLIA SERRATA)树脂提取物、蔬食埃塔棕(EUTERPE OLERACEA)果提取物、狭夜越桔(VACCINIUM ANGUSTIFOULIUM)果提取物、余甘子(PHYLLANTHUS EMBLICA)果提取物、酵母菌/大麦籽发酵产物滤液、乳酸杆菌/梨汁发酵产物滤液、红曲(MONASCUS)/大米发酵产物、酵母菌/马铃薯提取物发酵产物滤液、酵母菌属/木酸杆菌/红茶发酵产物、乳酸杆菌/大豆发酵产物提取物、乳酸杆菌/凤眼兰发酵产物、乳酸杆菌/黑麦发酵细粉发酵产物、乳酸杆菌/人参根发酵产物滤液、白苏(PERILLA FRUTESCEN)叶提取物、菠菜(SPINACIA OLERACEA)叶提取物、菖蒲(ACORUS CALAMUS)根提取物、赤豆(PHASEOLUS ANGULARIS)籽提取物、大车前(PLANTAGO MAJOR)籽提取物、大蕉(MUSA SAPIENTUM)果提取物、地黄(REHMANNIA GLUTINOSA)提取物、钝叶决明(CASSIA OBTUSIFOLIA)籽提取物、番木瓜(CARICA PAPAYA)果提取物、甘薯(IPOMOEA BATATAS)根提取物、葛枣猕猴桃(ACTINIDIA POLYGAMA)果提取物、枸杞(LYCIUM CHINENSE)果提取物、光果甘草(GLYCYRRHIZA GLABRA)根提取物、红花(CARTHAMUS TINCTORIUS)花提取物、胡萝卜(DAUCUS CAROTA SATIVA)根提取物、黄瓜(CUCUMIS SATIVUS)果提取物、灰树花(GRIFOLA FRONDOSA)子实体提取物、鸡桑(MORUS BOMBYCIS)叶提取物、鸡爪槭(ACER PALMATU)叶提取物、积雪草(CENTELLA ASIATICA)提取物、稷(PANICUM MILIACEUM)籽提取物、姜黄(CURCUMA LONGA)根提取物、荆芥(SCHIZONEPETA TENUIFOLIA)提取物、桔梗(PLATYCODON GRANDIFLORUM)根提取物、菊苣(CICHORIUM INTYBUS)根提取物、卷心菜(BRASSICA OLERACEA CAPITATA)叶提取物、魁蒿(ARTEMISIA PRINCEPS)叶提取物、栝楼(TRICHOSANTHES KIRILOWII)根提取物、辣薄荷(MENTHA PIPERITA)花/叶/茎提取物、李(PRUNUS SALICINA)果提取物、莲(NELUMBO NUCIFERA)根提取物、罗勒(OCIMUM BASILICUM)叶提取物、萝卜(RAPHANUS SATIVUS)根提取物、马齿苋(PORTULACA OLERACEA)提取物、迷迭香(ROSMARINUS OFFICINALIS)叶提取物、欧活血丹(GLECHOMA HEDERACEA)提取物、欧蒲公英(TARAXACUM OFFICINALE)叶提取物、枇杷(ERIOBOTRYA JAPONICA)叶提取物、苹果(PYRUS MALUS)果提取物、裙带菜(UNDARIA PINNATIFIDA)提取物、忍冬(LONICERA JAPONICA)花提取物、山茶(CAMELLIA JAPONICA)叶乳酸杆HELIANTHUS ANNUUS)籽提取物 EGUS CUNEATA)籽提取物、知母(ANEMARRHENA ASPHODELOIDES)根提取物、麝香草(THYMUS VULGARIS)叶提取物、柿(DIOSPYROS KAKI)果提取物、蒜(ALLIUM SATIVUM)鳞茎提取物、桃(PRUNUS PERSICA)果提取物、甜菜(BETA VULGARIS)根提取物、维式熊竹(SASA VEITCHII)叶提取物、温州蜜柑(CITRUS UNSHIU)果皮提取物、问荆(EQUISETUM ARVENSE)提取物、无花果(FICUS CARICA)果提取物、芜菁(BRASSICA RAPA)叶提取物、西瓜(CITRULLUS LANATUS)果提取物、纤细老鹳草(GERANIUM ROBERTIANUM)提取物、香橙(CITRUS JUNOS)果提取物、香蜂花(MELISSA OFFICINALIS)提取物、香菇(LENTINUS EDODES)提取物、香柠檬叶(CITRUS AURANTIUM BERGAMIA)'叶提取物、向日葵籽(HELIANTHUS ANNUUS)籽提取物、杏(PRUNUS ARMWNIACA)果提取物、萱草(HEMEROCALLIS FULVA)花提取物、羊乳(CODONOPSIS LANCEOLATA)根提取物、洋葱(ALLIUM CEPA)鳞茎提取物、野山楂(CRATAEGUS CUNEATA)果提取物、银杏(GINKGO BILOBA)坚果提取物、鱼腥草(HOUTTUYNIA CORDATA)提取物、芝麻(SESAMUM INDICUM)籽提取物、知母(ANEMARRHENA ASPHODELOIDES)根提取物、X、Y'''
        ingredient_list = ingredient.split('、')
        ingredient_list_extract = []
        for i in ingredient_list:
            if '提取物' in i:
                ingredient_list_extract.append(i)
        print(ingredient_list_extract)
        return ingredient_list_extract


if __name__ == '__main__':
    start_time = time.time()
    spider = Ingredient_Spider()
    spider.run()
    end_time = time.time()
    print('执行时间:%.2f' % (end_time - start_time))
