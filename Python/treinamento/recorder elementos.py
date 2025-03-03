from pywinauto_recorder import Recorder
from pathlib import Path

def iniciar_gravacao():
    """Inicia a gravação de interações com a interface gráfica do Windows."""
    recorder = Recorder()
    recorder.start_recording()

    print("🔴 Gravação iniciada. Realize as ações que deseja capturar.")
    
    try:
        input("Pressione Enter para parar a gravação...")  # Aguarda o usuário pressionar Enter
    except KeyboardInterrupt:
        print("\n⏹ Interrompido manualmente.")
    
    # Para a gravação corretamente
    script = recorder.stop_recording()

    # Caminho para salvar o script gerado
    output_path = Path.home() / "Documents" / "treinamento" / "script_gerado.py"

    if script:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(str(script))  # Converter em string antes de salvar
        print(f"✅ Ações gravadas e script salvo como '{output_path}'.")
    else:
        print("⚠ Nenhuma ação foi capturada durante a gravação.")

if __name__ == "__main__":
    iniciar_gravacao()
