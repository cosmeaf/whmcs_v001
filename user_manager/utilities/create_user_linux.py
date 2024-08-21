import subprocess
import uuid
import random
import string

def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for i in range(length))

def generate_linux_user():
    username = f'user{str(uuid.uuid4().int)[:6]}'
    password = generate_random_password()
    home_directory = f'/var/www/members/{username}'

    try:
        # Criar o usuário no Linux com o diretório home especificado
        subprocess.run(['sudo', 'useradd', '-m', '-d', home_directory, '-s', '/bin/bash', username], check=True)
        subprocess.run(['echo', f'{username}:{password}', '|', 'sudo', 'chpasswd'], shell=True, check=True)

        # Adicionar o usuário ao grupo www-data
        subprocess.run(['sudo', 'usermod', '-aG', 'www-data', username], check=True)

        # Obter UID e GID
        uid = subprocess.run(['id', '-u', username], capture_output=True, text=True).stdout.strip()
        gid = subprocess.run(['id', '-g', username], capture_output=True, text=True).stdout.strip()

        # Corrigir permissões do diretório home
        subprocess.run(['sudo', 'chown', 'www-data:www-data', '-R', home_directory], check=True)

        return {
            'username': username,
            'password': password,
            'uid': int(uid),
            'gid': int(gid),
            'home_directory': home_directory,
            'shell': '/bin/bash'
        }
    except subprocess.CalledProcessError as e:
        print(f"Error creating Linux user: {e}")
        return None