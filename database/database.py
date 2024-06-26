#from services.code_casar import caesar_decod, caesar

# Создаем шаблон заполнения словаря с пользователями
user_dict_template: dict = {'page': 1,
                            'bot_secret': '',
                            'chapter': 1,
                            'task': ''}

# Инициализируем "базу данных"
users_db: dict = {}

task_db: dict = {1: {1: ['СЛОН', 'ЖИРАФ', 'МОЛОКО']},
                2: {1: 'Река времен в своем стремлень\n'
                        'Уносит все дела людей\n'
                        'И топит в пропасти забвенья\n'
                        'Народы, царства и царей.\n'
                        'А если что и остается\n'
                        'Чрез звуки лиры и трубы,\n'
                        'То вечности жерлом пожрется\n'
                        'И общей не уйдет судьбы.\n',
                    2:  'ВлекисуровуюмечтУ,\n'
                        'дАйутомленнойреЧи,\n'
                        'ваДимъиэтудальИту,\n'
                        'дарИнастаромъВече\n'
                        'себеМгновениЕогня,\n'
                        'дайсмУтестеНыволи.\n'
                        'тыискуШениЕкремня:\n'
                        'затмениЕоШибкудня-\n'
                        'троньискРоюдоболи!\n'}}

tasks_db: dict = {'with_answer' : ['code_caesar',
                                'decode_caesar',
                                'decode_atbash',
                                'code_atbash',
                                'decode_akros']}

photo_db = {1: {3: 'images/1p3.png',
                4: 'images/1-4.png',
                5: 'images/1-5.jpg',
                7: 'images/1-7.png',
                8: 'images/1-8.png',
                9: 'images/1-9.png',
                10: 'images/1-10.jpg',
                12: 'images/1-12.png'},
            2: {3:  'images/2-3.png',
                4:  'images/2-4.png',
                5:  'images/2-5.jpg',
                8:  'images/2-8.png',
                9:  'images/2-9.png',
                10: 'images/2-10.png',
                11: 'images/2-11.png',
                13: 'images/2-13.png',
                14: 'images/2-14.png',
                15: 'images/2-15.png',
                16: 'images/2-16.png',
                17: 'images/2-17.png',
                18: 'images/2-18.png',
                21: 'images/2-21.png',
                22: 'images/2-22.jpg',
                23: 'images/2-23.png'},
            3: {1:  'images/3-1.png',
                2:   'images/3-2.png',
                4:   'images/3-4.png',
                6:'images/3-6.png',
                7:'images/3-7.png',
                8:'images/3-8.png',
                10:'images/3-10.png',
               11:'images/3-11.jpg',
               13:'images/3-13.png',
               14:'images/3-14.png',
               15:'images/3-15.png',
               16:'images/3-16.png',
               17:'images/3-17.png',
               19:'images/3-19.png',
               20:'images/3-20.png',
               21:'images/3-21.png'},
            4: {1:'images/4-1.png',
               2:'images/4-2.png',
               3:'images/4-3.png',
               4:'images/4-4.png',
               5:'images/4-5.png',
               6:'images/4-6.png',
               7:'images/4-7.png',
               8:'images/4-8.png',
               10:'images/4-10.jpg'},
            5: {3:'images/5-3.png',
               4:'images/5-4.png',
               5:'images/5-5.png',
               6:'images/5-6.png',
               7:'images/5-7.png',
               8:'images/5-8.png',
               9:'images/5-9.jpg',
               10:'images/5-10.png',
               11:'images/5-11.png',
               13:'images/5-13.png',
               18:'images/5-18.png',
               22:'images/5-22.jpg',
               23:'images/5-23.jpg',
               24:'images/5-24.jpg',
               25:'images/5-25.png',
               26:'images/5-26.png'},
            6:{2:'images/6-2.png',
               3:'images/6-3.png',
               5:'images/6-4.png',
               6:'images/6-5.png',
               7:'images/6-9.jpg',
               12:'images/6-13.gif',
               13:'images/6-14.png',
               15:'images/6-16.jpg',
               16:'images/6-17.jpg',
               20:'images/6-21.jpg'},
            7:{4:'images/7-4.png',
               5:'images/7-5.png',
               7:'images/7-7.jpg',
               11:'images/7-11.png'},
            8:{2:'images/8-2.png',
               4:'images/8-4.jpg',
               5:'images/8-5.jpg',
               6:'images/8-6.jpg',
               7:'images/8-7.png',
               8:'images/8-8.jpg',
               9:'images/8-9.png',
               10:'images/8-10.png',
               12:'images/8-11.png',
               13:'images/8-12.jpg',
               14:'images/8-13.png',},
            9:{2:'images/9-2.jpg',
               3:'images/9-3.png',
               4:'images/9-4.png',
               5:'images/9-5.png',
               10:'images/9-10.png',},
            10:{1:'images/10-1.jpg',
                2:'images/10-2.png',
                5:'images/10-5.png',
                7:'images/10-7.gif'},
            11:{ 8:'images/11-7.png',
                10:'images/11-9.png',
                16:'images/11-15.png',
                20:'images/11-20.jpg',
                21:'images/11-21.png'},
            12:{3:'images/12-3.png',
                4:'images/12-4.png',
                6:'images/12-6.png',
                10:'images/12-10.png',
                11:'images/12-11.png',
                12:'images/12-12.png',
                13:'images/12-13.png'}}
                #14:'images/image114.png'
#                 7: 'images/image1p7.png',
#                 8: 'images/image1p8.png'},
#             2: {3: 'images/image2p3.png',
#                 5: 'images/image2p4.png',
#                 6: 'images/image2p5.png'},
#             3: {3: 'images/image3p3.png',
#                 5: 'images/image3p5.png',
#                 6: 'images/image3p6.png',
#                 7: 'images/image3p7.png',
#                 10: 'images/image3p10.png',
#                 12: 'images/image3p12.png',
#                 14: 'images/image3p14.png',
#                 16: 'images/image3p16.png',
#                 18: 'images/image3p18.png'},
#             4:  {2: 'images/image4p2.png'}}

#print(task_db[2][1])