import os
from .tool_function_lib import load_json_file, save_json_file


class Config:
    def __init__(self):
        self.data_folder = 'backend/data'
        self.save_folder = os.path.join(self.data_folder, 'save')
        self.history_folder = os.path.join(self.data_folder, 'history')
        self.standard_foods_file = os.path.join(self.save_folder, 'standard_foods.json')
        self.general_foods_file = os.path.join(self.save_folder, 'general_foods.json')
        self.standard_attributes_file = os.path.join(self.save_folder, 'standard_attributes.json')
        self.json_tree_folder = os.path.join(self.data_folder, 'jsonTreeFromExcel')
        self.excel_src_folder = os.path.join(self.data_folder, 'excelSrc')
        self.standard_foods_excel = os.path.join(self.excel_src_folder, 'standardFoods', '统一标准_食品_含同义词.xlsx')
        self.standard_attributes_excel = os.path.join(self.excel_src_folder, 'standardAttributes', '贵科院_属性.xlsx')
        self.general_foods_excel = os.path.join(self.excel_src_folder, 'generalFoods', '评估中心系统字典表--VV.xlsx')
        self.general_filed_sheetname = {'化学': '化学污染物食品分类', '微生物': '微生物食品分类', '暴发': '暴发食品分类'}
        self.id_file = os.path.join(self.save_folder, 'id.json')
        self.ids = load_json_file(self.id_file, default='obj')
        self.record_history = False
        os.makedirs(self.save_folder, exist_ok=True)
        os.makedirs(self.history_folder, exist_ok=True)
        os.makedirs(self.json_tree_folder, exist_ok=True)

    def generate_new_id(self, field):
        # 输入field名称，自动生成递增的id，例如输入'食品'，生成'食品_n'的id，且不会与已有id冲突
        # filed可以是“食品”、“属性”、“化学”、“微生物”等等
        new_id = 0
        if field in self.ids:
            new_id = self.ids[field] + 1
        self.ids[field] = new_id
        save_json_file(self.id_file, self.ids)
        return field + str(new_id)


CONFIG = Config()
