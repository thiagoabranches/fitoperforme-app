import fitz  # PyMuPDF
import os
import sys

# --- CORREÇÃO DE CODIFICAÇÃO PARA WINDOWS ---
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Configuração das páginas exatas das plantas no seu PDF
PAGINAS_PLANTAS = {
    "tribulus": 8,
    "maca": 13,
    "ashwagandha": 18,
    "mucuna": 24,
    "longjack": 29,
    "serenoa": 34,
    "ajuga": 39,
    "prunus": 43,
    "urtica": 48,
    "feno": 53,
    "tetradium": 58,
    "cyanotis": 63,
    "kaempferia": 67,
    "bulbine": 72
}

def criar_requirements():
    """Cria o arquivo requirements.txt necessário para o Streamlit Cloud"""
    conteudo = """streamlit
Pillow"""
    with open("requirements.txt", "w") as f:
        f.write(conteudo)
    print("[INFO] Arquivo 'requirements.txt' criado com sucesso (Item 2).")

def extrair():
    pdf_nome = "livro pm desempenho fisico 2025.pdf"
    
    if not os.path.exists(pdf_nome):
        print("[ERRO] Nao encontrei o arquivo PDF na pasta.")
        print(f"Certifique-se que o arquivo se chama: {pdf_nome}")
        return

    # Cria a pasta para as imagens
    if not os.path.exists("imagens_plantas"):
        os.makedirs("imagens_plantas")
        print("[INFO] Pasta 'imagens_plantas' criada.")

    try:
        print("[INFO] Lendo PDF... (Isso pode levar alguns segundos)")
        doc = fitz.open(pdf_nome)
        
        for planta_id, pagina_num in PAGINAS_PLANTAS.items():
            try:
                if pagina_num < len(doc):
                    page = doc.load_page(pagina_num)
                    # Matrix=2 garante alta qualidade na imagem
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    
                    caminho_saida = f"imagens_plantas/{planta_id}.png"
                    pix.save(caminho_saida)
                    print(f"[OK] Imagem salva: {caminho_saida}")
                else:
                    print(f"[AVISO] Pagina {pagina_num} nao existe no PDF.")
            except Exception as e:
                print(f"[ERRO] Falha ao salvar {planta_id}: {e}")
                
        print("\n[SUCESSO] Todas as imagens foram extraidas (Item 5)!")
        
    except Exception as e:
        print(f"[ERRO CRITICO] ao abrir o PDF: {e}")

if __name__ == "__main__":
    # 1. Gera o requirements.txt
    criar_requirements()
    
    # 2. Extrai as imagens
    extrair()
    
    print("\n--- PRONTO ---")
    print("Agora voce ja tem o 'requirements.txt' e a pasta 'imagens_plantas'.")
    print("Pode remover o PDF e subir para o GitHub.")