import flet as ft
import requests
import os
from bs4 import BeautifulSoup
from fpdf import FPDF

cor_cinza = "#1a1a1a"
cor_branca = "#ebebeb"
cor_azul = "#1968a8"
cor_vermelha = "#f22929"
cor_verde = "#18661f"
cor_transparente = ft.colors.TRANSPARENT
negrito = ft.FontWeight.BOLD
fonte = "Roboto"

def tela_geral(page: ft.Page):
    page.bgcolor = cor_cinza
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = ft.padding.all(0)
    page.title = "Descubra o código fonte do site."
    page.window.alignment = ft.alignment.center
    page.window.width = 400 # Largura
    page.window.height = 250 # Altura
    page.window.maximizable = False
    page.window.minimizable = False

    def baixar_codigo_fonte(url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            texto1_tela_atual.content.color = cor_vermelha
            texto1_tela_atual.content.value = f"Erro ao baixar código fonte: {e}"
            texto1_tela_atual.update()
            return None

    def remover_blur(html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            elementos_com_blur = soup.find_all(style=lambda value: value and "blur" in value)
            for elemento in elementos_com_blur:
                elemento.decompose()
            return str(soup)
        except Exception as e:
            texto1_tela_atual.content.color = cor_vermelha
            texto1_tela_atual.content.value = f"Erro ao remover blur: {e}"
            texto1_tela_atual.update()
            return html

    def criar_pdf_conteudo(html, url, pasta_destino):
        try:
            soup = BeautifulSoup(html, "html.parser")
            texto = soup.get_text()
            titulo = soup.title.string if soup.title else "conteudo_site"
            titulo = titulo.strip().replace("/", "-")
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"URL: {url}", ln=True, align='C')
            pdf.ln(10)
            for linha in texto.splitlines():
                linha = linha.strip()
                if linha:
                    try:
                        pdf.multi_cell(0, 10, linha.encode('latin-1', 'replace').decode('latin-1'))
                    except Exception as e:
                        texto1_tela_atual.content.color = cor_vermelha
                        texto1_tela_atual.content.value = f"Erro ao adicionar linha ao PDF: {e}"
                        texto1_tela_atual.update()
            nome_pdf = f"{titulo}.pdf"
            caminho_pdf = os.path.join(pasta_destino, nome_pdf)
            pdf.output(caminho_pdf)
            texto1_tela_atual.content.color = cor_verde
            texto1_tela_atual.content.value = f"PDF gerado em: {caminho_pdf}"
            texto1_tela_atual.update()
        except Exception as e:
            texto1_tela_atual.content.color = cor_vermelha
            texto1_tela_atual.content.value = f"Erro ao criar PDF: {e}"
            texto1_tela_atual.update()

    def gerenciador_download(e):
        texto1_tela_atual.content.color = cor_azul
        texto1_tela_atual.content.value = f"Aguarde..."
        texto1_tela_atual.update()
        url = entrada1_tela_atual.content.value
        if not os.path.exists("downloads_pdf"):
            os.makedirs("downloads_pdf")
        html = baixar_codigo_fonte(url)
        if html:
            html_sem_blur = remover_blur(html)
            criar_pdf_conteudo(html_sem_blur, url, "downloads_pdf")

    entrada1_tela_atual  = ft.Container(
        content=ft.TextField(
            text_align=ft.TextAlign.START, cursor_color=cor_branca, cursor_width=2, cursor_height=20,
            selection_color=cor_azul, text_size=14, text_vertical_align=0, label="Coloque seu Link", color=cor_branca,
            border_radius=15, border_width=2, border_color=cor_branca, text_style=ft.TextStyle(size=14,
            font_family=fonte, color=cor_branca), label_style=ft.TextStyle(size=16, font_family=fonte, color=cor_branca,
            weight=negrito)
        ),
        alignment=ft.alignment.center,
        width=350,
        height=40
    )

    botao1_tela_atual = ft.Container(
        content=ft.Text(
            value="Gerar PDF", text_align=ft.TextAlign.CENTER, font_family=fonte, size=16, weight=negrito,
            italic=True, color=cor_cinza
        ),
        alignment=ft.alignment.center,
        width=100,
        height=30,
        bgcolor=cor_branca,
        border_radius=15,
        on_click=gerenciador_download
    )

    texto1_tela_atual = ft.Container(
        content=ft.Text(
            value="", text_align=ft.TextAlign.CENTER, font_family=fonte, size=14, weight=negrito,
            italic=True, color=cor_verde
        ),
        alignment=ft.alignment.center_left,
        width=350,
        height=40
    )

    tela_atual = ft.Container(
        content=ft.Column(
            [
                entrada1_tela_atual,
                botao1_tela_atual,
                texto1_tela_atual
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center
    )

    page.add(tela_atual)

#ft.app(target=tela_geral)