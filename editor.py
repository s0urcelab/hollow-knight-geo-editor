import json
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from utils import SaveFileUtils
import zipfile
from datetime import datetime
from i18n import get_text

# 存档文件路径
SAVE_DIR = os.path.expandvars(r"%APPDATA%\..\LocalLow\Team Cherry\Hollow Knight")

class HollowKnightSaveEditor:
    def __init__(self):
        self.save_files = self._find_save_files()

    def _find_save_files(self):
        """Find all save files and group them by user number"""
        save_groups = {}
        
        # 遍历存档目录
        for filename in os.listdir(SAVE_DIR):
            # 匹配 user数字 开头的文件
            match = re.match(r'user(\d+)', filename)
            if match:
                user_num = int(match.group(1))
                if user_num not in save_groups:
                    save_groups[user_num] = []
                save_groups[user_num].append(os.path.join(SAVE_DIR, filename))
        
        return save_groups

    def get_main_save_file(self, save_files):
        """Get the main save file (user数字.dat) from a list of save files"""
        for filepath in save_files:
            if re.match(r'.*user\d+\.dat$', filepath):
                return filepath
        return None

    def load_save(self, filepath):
        """Load save file"""
        try:
            if not os.path.exists(filepath):
                print(f"Warning: Save file not found at: {filepath}")
                return None

            with open(filepath, 'rb') as f:
                data = f.read()
                
            save_data = SaveFileUtils.decrypt_save(data)
            
            # Validate JSON
            json_data = json.loads(save_data)
            return json_data
        except Exception as e:
            print(f"Warning: Failed to load save file {filepath}: {str(e)}")
            return None

    def save_save(self, save_data, filepath):
        """Save file"""
        try:
            # Validate JSON
            save_data_str = json.dumps(save_data)
            
            encrypted_data = SaveFileUtils.encrypt_save(save_data_str)
            with open(filepath, 'wb') as f:
                f.write(encrypted_data)
                    
            return True
        except Exception as e:
            print(f"Warning: Failed to save file {filepath}: {str(e)}")
            return False

    def get_geo(self, save_data):
        """Get geo value from save data"""
        try:
            return save_data.get('playerData', {}).get('geo', 0)
        except:
            return 0

    def set_geo(self, save_data, new_geo):
        """Set geo value in save data"""
        try:
            if 'playerData' not in save_data:
                save_data['playerData'] = {}
            save_data['playerData']['geo'] = new_geo
            return True
        except:
            return False

class SaveSlotScreen(ttk.Frame):
    def __init__(self, parent, on_slot_selected):
        super().__init__(parent)
        self.on_slot_selected = on_slot_selected
        self.editor = None
        self.setup_ui()

    def setup_ui(self):
        # 标题
        title_label = ttk.Label(self, text=get_text('title'), font=('', 16))
        title_label.pack(pady=20)

        # 主内容区
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)

        # 存档槽选择区
        slot_frame = ttk.LabelFrame(main_frame, text=get_text('save_slot'))
        slot_frame.pack(fill=tk.X, pady=10)

        self.save_slot_var = tk.StringVar()
        self.save_slot_combo = ttk.Combobox(slot_frame, textvariable=self.save_slot_var, state="readonly")
        self.save_slot_combo.pack(fill=tk.X, padx=10, pady=10)
        self.save_slot_combo.bind('<<ComboboxSelected>>', self.on_slot_changed)

        # 存档文件列表区
        file_frame = ttk.LabelFrame(main_frame, text=get_text('save_files'))
        file_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.file_list_frame = ttk.Frame(file_frame)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建Treeview
        columns = ('filename', 'size', 'modified')
        self.file_tree = ttk.Treeview(self.file_list_frame, columns=columns, show='headings', height=8)
        
        # 设置列标题
        self.file_tree.heading('filename', text=get_text('filename'))
        self.file_tree.heading('size', text=get_text('size'))
        self.file_tree.heading('modified', text=get_text('modified'))
        
        # 设置列宽
        self.file_tree.column('filename', width=150)
        self.file_tree.column('size', width=100)
        self.file_tree.column('modified', width=150)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.file_list_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        # 禁止选择
        self.file_tree.bind('<<TreeviewSelect>>', lambda e: 'break')
        
        # 布局
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 确认按钮
        self.confirm_button = ttk.Button(main_frame, text=get_text('confirm'), command=self.on_confirm)
        self.confirm_button.pack(pady=20)

    def load_save_slots(self, editor):
        """加载存档槽列表"""
        self.editor = editor
        if not editor.save_files:
            return
        
        save_slots = sorted(editor.save_files.keys())
        self.save_slot_combo['values'] = [f"user{slot}" for slot in save_slots]
        if save_slots:
            self.save_slot_combo.set(f"user{sorted(save_slots)[0]}")
            self.on_slot_changed(None)

    def on_slot_changed(self, event):
        """当选择存档槽时更新文件列表"""
        try:
            slot_text = self.save_slot_var.get()
            if not slot_text:
                return
            
            slot_num = int(slot_text.replace('user', ''))
            save_files = self.editor.save_files[slot_num]
            
            # 清空现有项目
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
            
            # 添加文件到列表
            for filepath in save_files:
                filename = os.path.basename(filepath)
                # 获取文件大小
                size = os.path.getsize(filepath)
                size_str = f"{size / 1024:.1f} KB"
                # 获取修改时间
                modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                modified_str = modified.strftime("%Y-%m-%d %H:%M:%S")
                
                self.file_tree.insert('', tk.END, values=(filename, size_str, modified_str))
            
        except Exception as e:
            messagebox.showerror(get_text('error'), str(e))

    def on_confirm(self):
        """确认选择存档槽"""
        try:
            slot_text = self.save_slot_var.get()
            if not slot_text:
                messagebox.showerror(get_text('error'), get_text('please_select_slot'))
                return
            
            slot_num = int(slot_text.replace('user', ''))
            self.on_slot_selected(slot_num)
        except Exception as e:
            messagebox.showerror(get_text('error'), f"{get_text('failed_to_load_slot')}{str(e)}")

class GeoEditorScreen(ttk.Frame):
    def __init__(self, parent, editor, save_files, on_back):
        super().__init__(parent)
        self.editor = editor
        self.save_files = save_files
        self.on_back = on_back
        self.current_save_data = None
        self.setup_ui()
        self.load_save_data()

    def setup_ui(self):
        # 标题栏
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        back_button = ttk.Button(title_frame, text=get_text('back'), command=self.on_back)
        back_button.pack(side=tk.LEFT)

        # 主内容区
        content_frame = ttk.Frame(self)
        content_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
        
        # 当前金钱显示
        ttk.Label(content_frame, text=get_text('current_geo')).pack(anchor=tk.W, pady=5)
        self.current_geo_label = ttk.Label(content_frame, text="0", font=('', 14))
        self.current_geo_label.pack(anchor=tk.W, pady=5)
        
        # 新金钱输入
        ttk.Label(content_frame, text=get_text('new_geo')).pack(anchor=tk.W, pady=5)
        self.new_geo_var = tk.StringVar()
        self.new_geo_entry = ttk.Entry(content_frame, textvariable=self.new_geo_var, font=('', 14))
        self.new_geo_entry.pack(fill=tk.X, pady=5)
        
        # 更新按钮
        self.update_button = ttk.Button(content_frame, text=get_text('update_geo'), command=self.update_geo)
        self.update_button.pack(pady=20)

    def load_save_data(self):
        """加载存档数据"""
        try:
            # 读取主存档文件
            main_save_file = self.editor.get_main_save_file(self.save_files)
            if not main_save_file:
                messagebox.showerror(get_text('error'), get_text('main_save_not_found'))
                return
            
            # 加载存档数据
            self.current_save_data = self.editor.load_save(main_save_file)
            if not self.current_save_data:
                messagebox.showerror(get_text('error'), get_text('failed_to_load'))
                return
            
            # 显示当前金钱数
            geo = self.editor.get_geo(self.current_save_data)
            self.current_geo_label.config(text=str(geo))
            self.new_geo_var.set(str(geo))
            
        except Exception as e:
            messagebox.showerror(get_text('error'), f"{get_text('failed_to_load')}{str(e)}")

    def update_geo(self):
        """更新金钱数"""
        try:
            if not self.current_save_data:
                messagebox.showerror(get_text('error'), get_text('failed_to_load'))
                return
            
            # 获取新的金钱数
            try:
                new_geo = int(self.new_geo_var.get())
                if new_geo < 0:
                    raise ValueError(get_text('geo_cannot_be_negative'))
            except ValueError as e:
                messagebox.showerror(get_text('error'), get_text('please_enter_valid_number'))
                return
            
            # 创建备份
            if not SaveFileUtils.create_backup(self.save_files, SAVE_DIR):
                if not messagebox.askyesno(get_text('warning'), get_text('failed_to_create_backup')):
                    return
            
            # 更新所有存档文件
            success = True
            for filepath in self.save_files:
                save_data = self.editor.load_save(filepath)
                if save_data:
                    if self.editor.set_geo(save_data, new_geo):
                        if not self.editor.save_save(save_data, filepath):
                            success = False
                    else:
                        success = False
            
            if success:
                self.current_geo_label.config(text=str(new_geo))
                messagebox.showinfo(get_text('title'), get_text('update_success'))
            else:
                messagebox.showerror(get_text('error'), get_text('failed_to_update_some'))
        except Exception as e:
            messagebox.showerror(get_text('error'), f"{get_text('failed_to_update')}{str(e)}")

class SaveEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(get_text('title'))
        self.root.geometry("600x500")
        
        # 设置程序图标
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {str(e)}")
        
        self.editor = HollowKnightSaveEditor()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面
        self.slot_screen = SaveSlotScreen(self.main_frame, self.on_slot_selected)
        self.geo_screen = None
        
        # 显示存档槽选择界面
        self.slot_screen.pack(fill=tk.BOTH, expand=True)
        self.slot_screen.load_save_slots(self.editor)

    def on_slot_selected(self, slot_num):
        """当选择存档槽时触发"""
        try:
            # 获取对应的存档文件
            save_files = self.editor.save_files[slot_num]
            
            # 尝试读取主存档文件
            main_save_file = self.editor.get_main_save_file(save_files)
            if not main_save_file:
                messagebox.showerror(get_text('error'), get_text('main_save_not_found'))
                return
                
            # 尝试加载存档数据
            save_data = self.editor.load_save(main_save_file)
            if not save_data:
                messagebox.showerror(get_text('error'), get_text('failed_to_load'))
                return
            
            # 创建并显示Geo编辑器界面
            self.slot_screen.pack_forget()
            self.geo_screen = GeoEditorScreen(self.main_frame, self.editor, save_files, self.show_slot_screen)
            self.geo_screen.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror(get_text('error'), f"{get_text('failed_to_load_slot')}{str(e)}")

    def show_slot_screen(self):
        """返回存档槽选择界面"""
        # 隐藏其他界面
        if self.geo_screen:
            self.geo_screen.pack_forget()
        
        # 显示存档槽选择界面
        self.slot_screen.pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = SaveEditorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 