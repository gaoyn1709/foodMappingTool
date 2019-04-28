import os
import re
import pandas as pd
from backend.lib.config import CONFIG
from backend.lib.tool_function_lib import save_json_file, load_json_file
from backend.lib.all_data import all_data
from backend.lib.basic_class import StandardFoodNode, StandardAttribute, GeneralFoodNode

food_json_tree_file = os.path.join(CONFIG.json_tree_folder, 'standardFoodTree.json')
food_code_to_id_file = os.path.join(CONFIG.json_tree_folder, 'standardFoodCode2SystemID.json')
attribute_json_tree_file = os.path.join(CONFIG.json_tree_folder, 'standardAttributeTree.json')
attribute_code_to_id_file = os.path.join(CONFIG.json_tree_folder, 'standardAttributeCode2SystemID.json')


def dfs(root, func):
    func(root)
    for child in root['children']:
        dfs(child, func)


def read_excel(file_path, sheet=None, skip_row=0):
    if sheet is None:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name=sheet)
    df = df[skip_row:]
    df = df.replace(pd.np.nan, '', regex=True)
    return df


def generate_standard_foods():
    def make_tree_with_synonyms(file_path, ID, NAME, CODE, SYNONYM_NUM, SYNONYM):
        # 统一标准的食品结点转化为树状json
        df = read_excel(file_path)
        cols = list(df.columns)
        start_index = cols.index(SYNONYM)
        i = 0
        root = {'id': 0, 'name': 'root', 'children': [], 'parent_id': -1, 'code': 'F', 'synonym_num': 0, 'synonyms': [],
                'path': []}
        parent_codes = [root['code']]
        nodes = {root['code']: root}
        while i < len(df):
            food_id = df[ID][i].item()
            name = df[NAME][i]
            code: str = df[CODE][i]
            synonym_num = df[SYNONYM_NUM][i].item()
            node = {'id': food_id, 'name': name, 'children': [], 'code': code,
                    'synonym_num': synonym_num, 'synonyms': []}
            for j in range(synonym_num):
                synonym = df[cols[start_index + j]][i]
                if synonym == '':
                    print('error in synonym of id: %d' % food_id)
                node['synonyms'].append(synonym)
            while not code.startswith(parent_codes[-1]):
                parent_codes.pop()
            parent_code = parent_codes[-1]
            parent_node = nodes[parent_code]
            node['parent_id'] = parent_node['id']
            node['path'] = parent_node['path'] + [name]
            nodes[code] = node
            parent_node['children'].append(node)
            parent_codes.append(code)
            i += 1
        return root

    food_tree = make_tree_with_synonyms(CONFIG.standard_foods_excel, ID='序号', NAME='一级分类名称', CODE='编码',
                                        SYNONYM_NUM='同义词数量',
                                        SYNONYM='同义词')

    save_json_file(attribute_json_tree_file, food_tree)
    # 根结点单独处理
    root_id = CONFIG.generate_new_id('食品')
    all_data.standard_foods[root_id] = StandardFoodNode(root_id, 'root', '')
    id_dict = {-1: root_id}  # excel中的id到实际系统id的映射

    # 其余结点DFS遍历进行插入操作即可
    code2id = {}

    def func(node):
        parent_id = id_dict[node['parent_id']]
        new_id = all_data.insert_standard_food(parent_id, node['name'])
        # 更新同义词
        synonym_with_notes = dict()
        for synonym in node['synonyms']:
            synonym_with_notes[synonym] = '百度百科'
        all_data.modify_standard_food_synonyms(new_id, synonym_with_notes)
        id_dict[node['id']] = new_id
        code2id[node['code']] = new_id

    dfs(food_tree, func)
    save_json_file(food_code_to_id_file, code2id)


def generate_standard_attributes():
    def build_attribute_tree(file_path):
        df = read_excel(file_path)
        ids = list(df['序号'])
        names = list(df['属性描述名称'])
        parents = list(df['上级编码'])
        codes = list(df['编码'])
        types = list(df['大类编码'])
        root = {'id': 0, 'name': 'root', 'children': [], 'code': '', 'parent_code': '', 'type': '', 'parent_id': -1}
        nodes = [root]
        added_id = set()
        while len(nodes) > 0:
            node = nodes[0]
            added_id.add(node['id'])
            nodes = nodes[1:]
            for i in range(len(df)):
                if parents[i] == node['code']:
                    child = {'id': ids[i], 'name': names[i], 'children': [], 'parent_code': parents[i],
                             'parent_id': node['id'], 'code': codes[i], 'type': types[i]}
                    node['children'].append(child)
                    nodes.append(child)
        not_added_id = [x for x in ids if x not in added_id]
        print('attributes of these ids are not added to the tree, check it!')
        print(not_added_id)
        return root

    attribute_tree = build_attribute_tree(CONFIG.standard_attributes_excel)
    save_json_file(food_json_tree_file, attribute_tree)
    # 根结点单独处理
    root_id = CONFIG.generate_new_id('属性')
    all_data.standard_attributes[root_id] = StandardAttribute(root_id, 'root', '')
    id_dict = {-1: root_id}  # excel中的id到实际系统id的映射
    code2id = {}

    # 其余结点DFS遍历进行插入操作即可
    def func(node):
        parent_id = id_dict[node['parent_id']]
        new_id = all_data.insert_standard_attribute(parent_id, node['name'])
        id_dict[node['id']] = new_id
        code2id[node['code']] = new_id

    dfs(attribute_tree, func)
    save_json_file(attribute_code_to_id_file, code2id)


def generate_general_foods():
    field_sheetname = CONFIG.general_filed_sheetname
    food_code2id = load_json_file(food_code_to_id_file)
    attribute_code2id = load_json_file(attribute_code_to_id_file)

    def parse_ontology(s, food_codes_set: set, attribute_codes_set: set, sheet, line, name):
        # 正则解析各种乱七八糟的编码格式
        ontology = s.strip()
        if ontology == '':
            return [], []
        food_code_pattern = r'F0[A-Z]((([0-9]){2}((\.)?([0-9]){2})*)?)'
        attribute_code_pattern = r'A[A-Z]((([0-9]){2}((\.)?([0-9]){2})*)?)'
        food_codes = [''.join(x.group().split('.')) for x in re.finditer(food_code_pattern, s)]
        attribute_codes = [''.join(x.group().split('.')) for x in re.finditer(attribute_code_pattern, s)]
        err_position = 'Sheet: %s, Line: %d, Name: %s' % (sheet, line, name)
        err_flag = False
        food_code_res = []
        attribute_code_res = []
        for code in food_codes:
            if code not in food_codes_set:
                print('错误! 映射的食品编码不存在: %s' % code)
                err_flag = True
            else:
                food_code_res.append(code)
        for code in attribute_codes:
            if code not in attribute_codes_set:
                print('错误! 映射的属性编码不存在: %s' % code)
                err_flag = True
            else:
                attribute_code_res.append(code)
        if len(food_codes) == 0:
            if len(attribute_codes) == 0:
                if re.search(r'[\u4E00-\u9FA5]+', s) is None:
                    # 非汉字说明
                    err_flag = True
                    print('错误! 映射的编码格式错误: %s' % s)
            # else:
            #     print('警告! 仅映射了属性编码，没有食品编码，无法对应本体: %s' % '|'.join(attribute_codes))
        if err_flag:
            print('上述错误出现于：%s\n' % err_position)
        return food_code_res, attribute_code_res

    def make_tree_with_ontology(file_path, sheet, food_codes: set, attribute_codes: set, ID='主键', NAME='名称',
                                PARENT_ID='父ID', CODE='食品编码', PATH='路径', ONTOLOGY='分类+属性码'):
        df = read_excel(file_path, sheet=sheet, skip_row=1)
        ids = list(df[ID])
        names = list(df[NAME])
        parents = list(df[PARENT_ID])
        codes = list(df[CODE])
        paths = list(df[PATH])
        ontologys = list(df[ONTOLOGY])
        root = {'id': 0, 'parent_id': -1, 'name': 'root', 'code': '', 'ontology': [], 'attribute': [], 'children': []}
        nodes = [root]
        added_id = set()
        while len(nodes) > 0:
            node = nodes[0]
            added_id.add(node['id'])
            nodes = nodes[1:]
            for i in range(len(df)):
                if parents[i] == node['id']:
                    ontology, attribute = parse_ontology(ontologys[i], food_codes, attribute_codes, sheet, i + 2,
                                                         names[i])
                    child = {'id': ids[i], 'name': names[i], 'children': [], 'parent_id': parents[i], 'code': codes[i],
                             'path': paths[i], 'ontology': ontology, 'attribute': attribute}
                    node['children'].append(child)
                    nodes.append(child)
        not_added_id = [x for x in ids if x not in added_id]
        if len(not_added_id) > 0:
            print('错误! 在表 %s 中, 这些序号的结点无法被加入分类树中, 请检查它们和它们的父节点是否正确: %s\n\n\n' % (
                sheet, '|'.join([str(x) for x in not_added_id])))
        return root

    def get_ontology_codes():
        def get_codes(file, title='编码'):
            df = read_excel(file)
            codes = [''.join(x.strip().split('.')) for x in df[title]]
            codes_set = set(codes)
            if '' in codes_set:
                codes_set.remove('')
            for code in codes_set:
                if codes.count(code) > 1:
                    print('error in file %s! %s编码不唯一！' % (file, code))
            return codes_set

        return get_codes(CONFIG.standard_foods_excel), get_codes(CONFIG.standard_attributes_excel)

    food_code_set, attribute_code_set = get_ontology_codes()
    for field, sheet in field_sheetname.items():
        general_tree = make_tree_with_ontology(CONFIG.general_foods_excel, sheet, food_code_set, attribute_code_set)
        # 根结点单独处理
        root_id = CONFIG.generate_new_id(field)
        all_data.general_foods[field] = dict()
        all_data.general_foods[field][root_id] = GeneralFoodNode(root_id, 'root', '', field)
        id_dict = {-1: root_id}  # excel中的id到实际系统id的映射
        code2id = {}

        # 其余结点DFS遍历进行插入操作即可
        def func(node):
            parent_id = id_dict[node['parent_id']]
            new_id = all_data.insert_general_food(field, parent_id, node['name'])
            # 根据ontology及attribute更新映射
            id_dict[node['id']] = new_id
            code2id[node['code']] = new_id
            for standard_code in node['ontology']:
                standard_food_id = food_code2id[standard_code]
                attribute_ids = [attribute_code2id[code] for code in node['attribute']]
                all_data.add_mapping(field, new_id, standard_food_id, attribute_ids)

        dfs(general_tree, func)
        save_json_file(os.path.join(CONFIG.json_tree_folder, '%sCode2SystemID.json' % field), code2id)
        save_json_file(os.path.join(CONFIG.json_tree_folder, '%s.json' % field), general_tree)


def load_from_excel():
    generate_standard_foods()
    generate_standard_attributes()
    generate_general_foods()


if __name__ == '__main__':
    load_from_excel()
