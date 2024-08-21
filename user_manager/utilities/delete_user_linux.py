import subprocess


def delete_linux_user(username):
    try:
        # Divida o comando em seus componentes
        subprocess.run(["sudo", "userdel", "-rf", username], check=True)
        print(f"Usuário Linux {username} deletado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Falha ao deletar usuário Linux {username}: {e}")
        return False
