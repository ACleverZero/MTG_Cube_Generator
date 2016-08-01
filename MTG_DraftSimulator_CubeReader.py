##############################################################################################
#  MTG Cube Draft Drawing Engine
#  Lewis Patterson
#  
#  Code Overview:
#       - Code will draft MTG Booster packs off of an input cube set
#       - Code will read a MTG cube given a well defined structure.
#
#
#
#  Rev A: 06/25/2015  - Initial Development
#
#
#
##############################################################################################


import os
import math
import random as rnd


##############################################################################################
##############################################################################################
class CCubeReader():
    # --------------------------------------------
    def __init__(self,):
        self.key_names = {
                          'RARE'     : ['Rare','RARE','rare','Mythic','mythic','MYTHIC','R','M','r','m'],
                          'UNCOMMON' : ['Uncommon','UNCOMMON','UNC','U','u','unc','uncommon'],
                          'COMMON'   : ['Common','common','c','C','COMMON'],
                          }
        self.home_dir  = 'C:\\Users\\498623\\Documents\\python\\MTG_CUBE_GEN\\CubeSets\\'
        self.cube_sets = {}
    # --------------------------------------------
    def files_in_dir(self,):
        files_in_dir = os.listdir(self.home_dir)
        return files_in_dir
    # --------------------------------------------
    def reader(self,file_name):
        self.cube_sets[ file_name.split('.')[0] ] = {'RARE'    : {},
                                                     'UNCOMMON': {},
                                                     'COMMON'  : {},
                                                     }
        
        data_file = open(self.home_dir+file_name,'r')
        # look for header
        index = 0
        for row in data_file:
            #if index >0:
            data_row = row.replace('\n','').split(',')
            #print data_row
            for key in self.key_names.keys():
                for item in data_row:
                    if item in self.key_names[key]:
                        card_rarity = key
            card_count = 0
            for item in data_row:
                try:
                    card_count = int(item)
                except:
                    pass
            card_name    = data_row[0]
            try:
                self.cube_sets[ file_name.split('.')[0] ][card_rarity][card_name] = card_count + self.cube_sets[ file_name.split('.')[0] ][card_rarity][card_name]
            except:
                self.cube_sets[ file_name.split('.')[0] ][card_rarity][card_name] = card_count

        #print self.cube_sets[ file_name.split('.')[0] ]
    # --------------------------------------------
    def run(self):
        files = self.files_in_dir()
        for file in files:
            self.reader(file)
##############################################################################################
##############################################################################################
class CDraftEngine():
    # --------------------------------------------
    def __init__(self,master_list):

        self.master_list = master_list
        self.int_params  = {
                            'DEPLETE'        : True,
                            'PACKS_TO_MAKE'  : 3,
                            'DEBUG'          : False,
                            'BONUS_CARD'     : False,
                            }
        self.pack_params = {
                            'RARE_CNT': 1,
                            'UNCOMMON_CNT': 3,
                            'COMMON_CNT': 10,
                           }
        self.pack_gens   = {}
    # --------------------------------------------
    def draw_from_master(self,rarity_key):
        keys_list = []
        for key in self.master_list[rarity_key].keys():
            if self.master_list[rarity_key][key]>0:
                keys_list.append(key)
        draw_item = keys_list[ rnd.randint(0,len(keys_list)-1) ]
        if self.int_params['DEBUG'] == True:        
            print draw_item
        if self.int_params['DEPLETE'] == True:
            self.master_list[rarity_key][draw_item] = self.master_list[rarity_key][draw_item] -1
        return draw_item
    # --------------------------------------------
    def make_pack(self):
        pack = {'RARE'     : [],
                'UNCOMMON' : [],
                'COMMON'   : [],
                }
        try:
            pack_index = len(self.pack_gens.keys())
        except:
            pack_index = 0
            
        for rarity_index in pack.keys():
            for draw in range(0,self.pack_params[rarity_index+'_CNT']):
                if self.int_params['DEBUG'] == True:     
                    print'Drawing ',draw+1,'of ',self.pack_params[rarity_index+'_CNT']
                pack[rarity_index].append( self.draw_from_master(rarity_index) )
        # ---- Fix later ----
        if self.int_params['BONUS_CARD'] == True:
            pass
        # -------------------
        self.pack_gens[pack_index] = pack
    # --------------------------------------------
    def run(self):
        for pack in range(self.int_params['PACKS_TO_MAKE']):
            if self.int_params['DEBUG'] == True:
                print 'Making pack ',pack
            self.make_pack()
        #if self.int_params['DEBUG'] == True:
        for key in self.pack_gens:
            for rarity in self.pack_gens[key].keys():
                print'Pack ',key,' :',rarity,' ',self.pack_gens[key][rarity]
    # --------------------------------------------
##############################################################################################
##############################################################################################

CubeGen = CCubeReader()
CubeGen.run()
Draft = CDraftEngine(CubeGen.cube_sets['M15'])
Draft.int_params['PACKS_TO_MAKE'] = 50
Draft.run()

