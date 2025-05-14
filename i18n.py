import locale

# 获取系统语言
system_language = locale.getdefaultlocale()[0]

# 语言配置
LANGUAGES = {
    'zh_CN': {
        'title': '空洞骑士金钱修改器',
        'save_slot': '存档选择',
        'save_files': '存档包含文件',
        'filename': '文件名',
        'size': '大小',
        'modified': '修改时间',
        'confirm': '确认',
        'current_geo': '当前金钱:',
        'new_geo': '新的金钱数量:',
        'update_geo': '更新',
        'back': '← 返回',
        'error': '错误',
        'main_save_not_found': '未找到主存档文件！',
        'failed_to_load': '加载存档文件失败！',
        'failed_to_load_slot': '加载存档失败：',
        'please_select_slot': '请选择存档！',
        'please_enter_valid_number': '请输入有效的数字！',
        'geo_cannot_be_negative': '金钱数量不能为负数',
        'failed_to_update': '更新金钱失败：',
        'failed_to_update_some': '部分存档文件更新失败！',
        'update_success': '金钱更新成功！',
        'failed_to_create_backup': '创建备份失败。是否继续？',
        'warning': '警告'
    },
    'en_US': {
        'title': 'Hollow Knight Geo Editor',
        'save_slot': 'Save Slot',
        'save_files': 'Save Files',
        'filename': 'Filename',
        'size': 'Size',
        'modified': 'Modified',
        'confirm': 'Confirm',
        'current_geo': 'Current Geo:',
        'new_geo': 'New Geo Amount:',
        'update_geo': 'Update Geo',
        'back': '← Back',
        'error': 'Error',
        'main_save_not_found': 'Main save file not found!',
        'failed_to_load': 'Failed to load save file!',
        'failed_to_load_slot': 'Failed to load save slot:',
        'please_select_slot': 'Please select a save slot!',
        'please_enter_valid_number': 'Please enter a valid number!',
        'geo_cannot_be_negative': 'Geo amount cannot be negative',
        'failed_to_update': 'Failed to update geo:',
        'failed_to_update_some': 'Failed to update some save files!',
        'update_success': 'Geo updated successfully!',
        'failed_to_create_backup': 'Failed to create backup. Do you want to continue?',
        'warning': 'Warning'
    }
}

def get_text(key):
    """获取当前语言的文本"""
    lang = 'zh_CN' if system_language.startswith('zh') else 'en_US'
    return LANGUAGES[lang].get(key, key) 