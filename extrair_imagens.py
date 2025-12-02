import fitz  # PyMuPDF
import os

# Configuração das Plantas e suas páginas (Baseado no seu App)
# ID: Página (Lembre-se: O Python conta do 0. Se no PDF reader é pg 9, aqui é 8)
PAGINAS_PLANTAS = {
    "tribulus": 8,     # Página visual do Tribulus
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

def extrair():
    pdf_nome = "livro pm desempenho fisico 2025.pdf"
    
    if not os.path.exists(pdf_nome):
        print(f"ERRO: Não encontrei o arquivo '{pdf_nome}' na pasta.")
        return

    # Cria a pasta para as imagens se não existir
    if not os.path.exists("imagens_plantas"):
        os.makedirs("imagens_plantas")
        print("Pasta 'imagens_plantas' criada.")

    doc = fitz.open(pdf_nome)
    
    print("Iniciando extração em alta qualidade...")
    
    for planta_id, pagina_num in PAGINAS_PLANTAS.items():
        try:
            if pagina_num < len(doc):
                page = doc.load_page(pagina_num)
                # Matrix=2 garante alta resolução (2x zoom antes de salvar)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                
                caminho_saida = f"imagens_plantas/{planta_id}.png"
                pix.save(caminho_saida)
                print(f"✅ Salvo: {caminho_saida}")
            else:
                print(f"⚠️ Página {pagina_num} fora do limite para {planta_id}")
        except Exception as e:
            print(f"❌ Erro em {planta_id}: {e}")

    print("\nConcluído! Agora você pode deletar o PDF da pasta do projeto se quiser (mas guarde um backup!).")

if __name__ == "__main__":
    extrair()