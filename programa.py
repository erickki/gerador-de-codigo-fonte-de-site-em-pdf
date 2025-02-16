import flet as ft

from build.tela_geral import tela_geral

def programa(page: ft.Page):
    tela_geral(page)

ft.app(target=programa)