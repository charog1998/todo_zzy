from datetime import datetime
import os
import time
import tkinter as tk
from tkinter import END, ttk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo
import pygetwindow as gw
import pyautogui
from PIL import Image, ImageTk

from plan import Plan
from sql_part import select_by_id, select_by_topic, delete_by_id,insert,replace


class MainWindow:
    def __init__(self):
        self.main_frame = tk.Tk()
        self.planlist = []

    def set_window_position(self):
        screen_width = self.main_frame.winfo_screenwidth()  # 获取屏幕宽度
        screen_height = self.main_frame.winfo_screenheight()  # 获取屏幕高度
        width = 800
        height = 600
        gm_str = "%dx%d+%d+%d" % (
            width,
            height,
            (screen_width - width) / 2,
            (screen_height - 1.2 * height) / 2,
        )
        self.main_frame.geometry(gm_str)

    def config_for_main_window(self):
        self.main_frame.resizable(width=True, height=True)  # 设置界面大小不可调
        self.main_frame.title("todo_zzy")

    def set_panel(self):
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        Button_new_plan = tk.Button(
            self.top_frame, text="新增计划", command=self.new_plan
        )
        Button_new_plan.pack(side=tk.LEFT, fill=tk.NONE, padx=5, pady=5)

        Button_deleted_selected = tk.Button(
            self.top_frame, text="删除选中", command=self.delete_selected
        )
        Button_deleted_selected.pack(side=tk.LEFT, fill=tk.NONE, padx=5, pady=5)

        self.TreeView_Main = ttk.Treeview(self.main_frame, show="tree")
        self.TreeView_Main.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.TreeView_Main.configure(show="headings")
        self.TreeView_Main.configure(selectmode="extended")

        self.TreeView_Main["columns"] = ("主题", "截止日期", "状态")
        self.TreeView_Main.column("主题", width=300)
        self.TreeView_Main.column("截止日期", width=200)
        self.TreeView_Main.column("状态", width=100)

        self.TreeView_Main.heading("主题", text="主题")
        self.TreeView_Main.heading("截止日期", text="截止日期")
        self.TreeView_Main.heading("状态", text="状态")

        self.TreeView_Main.bind("<Double-1>", self.on_double_click)

        self.planlist = select_by_topic()
        for plan in self.planlist:
            self.TreeView_Main.insert(
                "",
                END,
                iid=plan.id,
                values=(
                    plan.topic,
                    plan.deadline.strftime(r"%Y-%m-%d"),
                    "已完成" if plan.state else "未完成",
                ),
            )

        self.botbutton_frame = tk.Frame(self.main_frame)
        self.botbutton_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        Button_SelectAll = tk.Button(
            self.botbutton_frame, text="全选", command=self.select_all
        )
        Button_SelectAll.pack(side=tk.LEFT, fill=tk.NONE, padx=5, pady=5)

        Button_SelectAll = tk.Button(
            self.botbutton_frame, text="反选", command=self.select_toggle
        )
        Button_SelectAll.pack(side=tk.LEFT, fill=tk.NONE, padx=5, pady=5)

    def show(self):
        self.main_frame.destroy()
        self.main_frame = tk.Tk()
        self.set_window_position()
        self.config_for_main_window()
        self.set_panel()
        self.main_frame.mainloop()

    def close(self):
        if self.main_frame == None:
            print("未显示界面")
        else:
            self.main_frame.destroy()

    def on_double_click(self, event):
        if self.TreeView_Main.selection():
            item = self.TreeView_Main.selection()[0]
            plan_selected = select_by_id(item)
            self.close()
            planinfo_window = Plan_window(plan_selected)
            planinfo_window.show()

    def get_selected_plans(self):
        selected_tuple = self.TreeView_Main.selection()
        return list(selected_tuple)

    def get_plan_by_topic(self, topic):
        for plan in self.planlist:
            if plan.topic == topic:
                return plan

    def select_all(self):
        """
        全选
        """
        sel_list = []
        for item in self.TreeView_Main.get_children():
            sel_list.append(item)
        self.TreeView_Main.selection_set(sel_list)

    def select_toggle(self):
        """
        反选
        """
        sel_list = []
        for item in self.TreeView_Main.get_children():
            sel_list.append(item)
        self.TreeView_Main.selection_toggle(sel_list)

    def new_plan(self):
        self.close()
        print("new plan")
        newplan_window = Plan_window()
        newplan_window.show()

    def delete_selected(self):
        selected_plans = self.get_selected_plans()
        for id in selected_plans:
            delete_by_id(int(id))
        self.show()


class Plan_window:
    def __init__(self, plan: Plan = Plan()):
        self.main_frame = tk.Tk()
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close)
        self.plan = plan
        self.current_windows = [""]
        titles = gw.getAllTitles()
        self.current_windows = []
        for x in titles:
            if x:
                self.current_windows.append(x)

    def set_window_position(self):
        screen_width = self.main_frame.winfo_screenwidth()  # 获取屏幕宽度
        screen_height = self.main_frame.winfo_screenheight()  # 获取屏幕高度
        self.width = screen_width * 0.8
        self.height = screen_height * 0.8
        gm_str = "%dx%d+%d+%d" % (
            self.width,
            self.height,
            (screen_width - self.width) / 2,
            (screen_height - 1.2 * self.height) / 2,
        )
        self.main_frame.geometry(gm_str)

    def config_for_main_window(self):
        self.main_frame.resizable(width=True, height=True)  # 设置界面大小可调
        if self.plan.id:
            self.main_frame.title(self.plan.topic)
        else:
            self.main_frame.title("新建计划")

    def set_panel(self):
        self.left_frame = tk.Frame(self.main_frame, width=self.width / 2)
        self.label_topic = tk.Label(self.left_frame, text="主题", font=10, anchor="w")
        self.label_topic.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.entry_topic = tk.Entry(self.left_frame)
        self.entry_topic.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )
        self.entry_topic.insert(tk.END, str(self.plan.topic) if self.plan.topic else "")

        self.label_description = tk.Label(
            self.left_frame, text="描述", font=10, anchor="w"
        )
        self.label_description.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.entry_description = tk.Entry(self.left_frame)
        self.entry_description.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )
        self.entry_description.insert(
            tk.END, str(self.plan.description) if self.plan.description else ""
        )

        self.label_ddl = tk.Label(self.left_frame, text="结束日期", font=10, anchor="w")
        self.label_ddl.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.entry_ddl = tk.Entry(self.left_frame)
        self.entry_ddl.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )
        if self.plan.deadline:
            self.entry_ddl.insert(tk.END, self.plan.deadline.strftime(r"%Y-%m-%d"))
        else:
            self.entry_ddl.insert(tk.END, datetime.today().strftime(r"%Y-%m-%d"))

        self.label_state = tk.Label(
            self.left_frame,
            text="已完成" if self.plan.state else "未完成",
            font=10,
            anchor="w",
        )
        self.label_state.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )

        self.button_state_toggle = tk.Button(
            self.left_frame, font=10, text="切换完成状态", command=self.state_toggle
        )
        self.button_state_toggle.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )

        self.label_cycle = tk.Label(self.left_frame, text="周期", font=10, anchor="w")
        self.label_cycle.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        cycle_options = ["不重复", "每天", "每周", "每月"]
        po_map = {0: "不重复", 1: "每天", 7: "每周", 30: "每月"}
        selected_option = tk.StringVar(self.left_frame)
        if self.plan.cycle:
            selected_option.set(po_map.get(self.plan.cycle))
        else:
            selected_option.set(cycle_options[0])

        self.option_cycle = tk.OptionMenu(
            self.left_frame,
            selected_option,
            *cycle_options,
            command=lambda value: self.on_option_change(value)
        )
        self.option_cycle.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.label_cycle = tk.Label(
            self.left_frame, text="相关资源：", font=10, anchor="w"
        )
        self.label_cycle.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.left_buttons_frame = tk.Frame(self.left_frame)
        self.left_buttons_frame.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )
        self.button_add_local_dir = tk.Button(
            self.left_buttons_frame, font=8, text="文件夹", command=self.add_local_dir
        )
        self.button_add_local_dir.pack(
            side=tk.LEFT, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )

        self.button_add_local_file = tk.Button(
            self.left_buttons_frame, font=8, text="文件", command=self.add_local_file
        )
        self.button_add_local_file.pack(
            side=tk.LEFT, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )

        self.button_add_online = tk.Button(
            self.left_buttons_frame, font=8, text="添加网址", command=self.add_online
        )
        self.button_add_online.pack(
            side=tk.LEFT, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )

        self.entry_online = tk.Entry(self.left_buttons_frame)
        self.entry_online.pack(
            side=tk.LEFT, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )
        self.entry_online.insert(tk.END, "在此处粘贴网址后，点击左侧添加")

        self.url_frame = tk.Frame(self.left_frame)
        self.url_scrollbar = tk.Scrollbar(self.url_frame)
        self.url_listbox = tk.Listbox(
            self.url_frame, yscrollcommand=self.url_scrollbar.set
        )
        if isinstance(self.plan.url, str):
            for url in self.plan.url.split("#98#"):
                self.url_listbox.insert(tk.END, url)

        self.url_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.url_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="w")
        self.url_frame.pack(side=tk.TOP, fill=tk.X, expand=False, anchor="w")

        self.url_scrollbar.config(command=self.url_listbox.yview)
        self.url_listbox.config(yscrollcommand=self.url_scrollbar.set)
        self.url_listbox.bind("<Double-1>", self.url_double_click)

        self.left_frame.pack(
            side=tk.LEFT, fill=tk.Y, expand=False, anchor="nw", padx=10, pady=5
        )

        self.button_clear_all = tk.Button(
            self.left_frame, font=8, text="清空", command=self.clear_all
        )
        self.button_clear_all.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=5, pady=5
        )

        self.img_frame = tk.Frame(self.main_frame)

        self.label_cycle = tk.Label(self.img_frame, text="截图：", font=10, anchor="w")
        self.label_cycle.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.img_buttons_frame = tk.Frame(self.img_frame)
        self.img_buttons_frame.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.selected_window = tk.StringVar(self.main_frame)
        self.selected_window.set(self.current_windows[0])
        self.option_windows = tk.OptionMenu(
            self.img_frame, self.selected_window, *self.current_windows
        )
        self.option_windows.pack(
            side=tk.TOP, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.button_screenshot = tk.Button(
            self.img_buttons_frame, font=8, text="截取窗口", command=self.screenshot
        )
        self.button_screenshot.pack(
            side=tk.LEFT, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )

        self.button_refresh_winmessage = tk.Button(
            self.img_buttons_frame,
            font=8,
            text="重新获取窗口信息",
            command=self.refresh_winmessage,
        )
        self.button_refresh_winmessage.pack(
            side=tk.RIGHT, fill=tk.NONE, expand=False, anchor="w", padx=10, pady=5
        )
        if self.plan.imgList and isinstance(self.plan.imgList, str):
            image_path = self.plan.imgList.split("#98#")[-1]
            image = Image.open(image_path)
            image = image.resize((600, 400))
            self.label_image = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.img_frame, image=self.label_image)
            self.image_label.bind("<Double-1>", self.img_double_click)

        else:
            self.image_label = tk.Label(self.img_frame, text="无")
        self.image_label.pack(
            side=tk.TOP, fill=tk.BOTH, expand=True, anchor="w", padx=10, pady=5
        )

        self.img_frame.pack(
            side=tk.RIGHT, fill=tk.X, expand=True, anchor="ne", padx=10, pady=5
        )

        self.button_commit = tk.Button(self.img_frame, text="提交", command=self.commit)
        self.button_commit.pack(
            side=tk.BOTTOM, fill=tk.NONE, expand=False, padx=10, pady=5
        )

    def show(self):
        self.main_frame.destroy()
        self.main_frame = tk.Tk()
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close)
        self.set_window_position()
        self.config_for_main_window()
        self.set_panel()
        self.main_frame.mainloop()

    def close(self):
        if self.main_frame == None:
            print("未显示界面")
        else:
            self.main_frame.destroy()
            main_window = MainWindow()
            main_window.show()

    def on_option_change(self, value):
        op_map = {"不重复": 0, "每天": 1, "每周": 7, "每月": 30}
        self.plan.cycle = op_map.get(value)

    def state_toggle(self):
        self.plan.state = False if self.plan.state else True
        self.label_state = tk.Label(
            self.main_frame,
            text="已完成" if self.plan.state else "未完成",
            font=10,
            anchor="w",
        )
        self.update_plan()
        self.show()

    def add_local_dir(self):
        s = askdirectory()
        url = self.plan.url
        if url:
            url += "#98#"
            url += s
        else:
            url = s
        self.plan.url = url
        self.update_plan()
        self.show()

    def add_local_file(self):
        s = askopenfilename()
        url = self.plan.url
        if url:
            url += "#98#"
            url += s
        else:
            url = s
        self.plan.url = url
        self.update_plan()
        self.show()

    def add_online(self):
        s = self.entry_online.get()
        url = self.plan.url
        if url:
            url += "#98#"
            url += s
        else:
            url = s
        self.plan.url = url
        self.update_plan()
        self.show()

    def clear_all(self):
        self.plan.url = None
        self.update_plan()
        self.show()

    def screenshot(self):
        self.main_frame.wm_state("iconic")
        time.sleep(1)
        w = self.selected_window.get()
        window_selected = gw.getWindowsWithTitle(w)[0]
        left, top, width, height = (
            window_selected.left,
            window_selected.top,
            window_selected.width,
            window_selected.height,
        )
        img = pyautogui.screenshot(region=[left, top, width, height])
        if not os.path.exists(os.path.join(os.path.curdir, "temp_img")):
            os.mkdir(os.path.join(os.path.curdir, "temp_img"))
        img.save(os.path.join(os.path.curdir, "temp_img/screenshot.png"))
        self.plan.imgList = os.path.join(os.path.curdir, "temp_img/screenshot.png")
        self.update_plan()
        self.show()

    def refresh_winmessage(self):
        titles = gw.getAllTitles()
        self.current_windows = []
        for x in titles:
            if x:
                self.current_windows.append(x)
        self.update_plan()
        self.show()

    def commit(self):
        self.update_plan()
        temp_img_path = self.plan.imgList
        pwd = os.path.curdir
        img_dir_path = os.path.join(
            pwd,
            "imgs",
            str(self.plan.id) if self.plan.id else datetime.now().strftime(r"%Y%m%d%H%M%S"),
        )
        if not os.path.exists(img_dir_path):
            os.mkdir(img_dir_path)
        new_img_path = os.path.join(img_dir_path, "scrensnshot.png")
        os.remove(new_img_path)
        os.renames(old=temp_img_path, new=new_img_path)
        self.plan.imgList = new_img_path

        try:
            if self.plan.id:
                replace(self.plan)
            else:
                insert(self.plan)
        except Exception as e:
            showinfo(title="写入数据时出错", message=str(e))
        else:
            showinfo(title="", message="写入成功")

    def img_double_click(self, event):
        if isinstance(self.plan.imgList, str):
            img0_path = self.plan.imgList.split("#98#")[0]
            if os.path.exists(img0_path):
                os.startfile(img0_path)

    def url_double_click(self, event):
        if self.url_listbox.selection_get():
            os.startfile(self.url_listbox.selection_get())

    def update_plan(self):
        """用来把现在面板中的信息写到plan里面去"""
        self.plan.topic = self.entry_topic.get()
        self.plan.description = self.entry_description.get()
        if self.plan.state == None:
            self.plan.state = False
        if self.plan.cycle == None:
            self.plan.cycle = 0

        y, m, d = self.entry_ddl.get().split("-")[:3]
        try:
            ddl = datetime(year=int(y), month=int(m), day=int(d))
            self.plan.deadline = ddl
        except Exception as e:
            showinfo(title="日期输入错误", message=str(e))
            if self.plan.deadline == None:
                self.plan.deadline = datetime.today()


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.show()
