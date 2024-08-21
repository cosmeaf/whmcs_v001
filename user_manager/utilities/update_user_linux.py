import subprocess
import sys

def update_linux_user(old_username, new_username):
    # Comando para modificar o nome de usuário no Linux
    command = ["sudo", "usermod", "-l", new_username, old_username]
    
    try:
        subprocess.run(command, check=True)
        print(f"Usuário Linux {old_username} atualizado para {new_username}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar usuário Linux: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: update_user_linux.py <old_username> <new_username>")
        sys.exit(1)
    
    old_username = sys.argv[1]
    new_username = sys.argv[2]
    update_linux_user(old_username, new_username)
