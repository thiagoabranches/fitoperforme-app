import os
import sys
from PIL import Image

# Forcar encoding UTF-8 para evitar erros no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def otimizar_imagens():
    pasta_origem = "imagens_plantas"
    
    if not os.path.exists(pasta_origem):
        print("[ERRO] Pasta 'imagens_plantas' nao encontrada.")
        return

    print("--- INICIANDO OTIMIZACAO ---")
    
    arquivos = os.listdir(pasta_origem)
    
    for arquivo in arquivos:
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            nome_sem_ext = os.path.splitext(arquivo)[0]
            
            try:
                # 1. Abre a imagem
                with Image.open(caminho_completo) as img:
                    img = img.convert('RGB')
                    img.thumbnail((800, 1200)) 
                    
                    # 2. Salva como JPG Otimizado
                    novo_caminho = os.path.join(pasta_origem, f"{nome_sem_ext}.jpg")
                    img.save(novo_caminho, "JPEG", quality=75, optimize=True)
                    
                    print(f"[OK] Otimizado: {novo_caminho}")
            
                # 3. Remove o arquivo pesado original (PNG)
                if caminho_completo != novo_caminho:
                    os.remove(caminho_completo)
                    
            except Exception as e:
                print(f"[FALHA] Erro ao processar {arquivo}: {e}")

    print("\n--- CONCLUIDO ---")
    print("Todas as imagens foram convertidas para JPG leve.")

if __name__ == "__main__":
    otimizar_imagens()
