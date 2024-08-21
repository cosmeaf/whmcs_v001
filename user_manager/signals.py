import os
import subprocess
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member, Domain
from user_manager.utilities.create_user_linux import generate_linux_user
from user_manager.utilities.delete_user_linux import delete_linux_user

@receiver(post_save, sender=User)
def create_user_linux(sender, instance, created, **kwargs):
    if created:
        user_data = generate_linux_user()
        
        if user_data:
            # Criar e associar o usuário Linux ao Member
            Member.objects.create(
                user=instance,
                username=user_data['username'],
                password=user_data['password'],  # Salvando a senha gerada
                uid=user_data['uid'],
                gid=user_data['gid'],
                home_directory=user_data['home_directory'],
                shell=user_data['shell'],
            )
            print(f"User {user_data['username']} created with UID {user_data['uid']}, GID {user_data['gid']}, and password saved")
        else:
            print("Failed to create Linux user")

@receiver(pre_delete, sender=User)
def exclude_user_django(sender, instance, **kwargs):
    try:
        # Buscar o usuário Linux associado ao usuário Django sendo excluído
        user_linux = Member.objects.get(user=instance)
        username = user_linux.username
        print(f"Found associated Linux user: {username}")
        
        # Tentar deletar o usuário Linux
        if delete_linux_user(username):
            print(f"Successfully deleted Linux user {username}")
        else:
            print(f"Failed to delete Linux user {username}")
    except Member.DoesNotExist:
        print(f"No associated Linux user found for Django user {instance.username}, skipping deletion.")

@receiver(post_save, sender=Domain)
def create_subdomain_directory(sender, instance, created, **kwargs):
    if created:
        subdomain_dir = instance.get_subdomain_directory()
        index_template_path = '/var/www/index.html'  # Caminho do arquivo de modelo

        try:
            # Criar o diretório do subdomínio se não existir
            if not os.path.exists(subdomain_dir):
                subprocess.run(['sudo', 'mkdir', '-p', subdomain_dir], check=True)
                subprocess.run(['sudo', 'chown', 'www-data:www-data', '-R', subdomain_dir], check=True)
                subprocess.run(['sudo', 'chmod', '755', '-R', subdomain_dir], check=True)
                print(f"Created subdomain directory: {subdomain_dir}")

            # Copiar o arquivo index.html para o diretório do subdomínio
            subprocess.run(['sudo', 'cp', index_template_path, subdomain_dir], check=True)
            subprocess.run(['sudo', 'chown', 'www-data:www-data', os.path.join(subdomain_dir, 'index.html')], check=True)
            print(f"Copied index.html to {subdomain_dir}")

            # Criar o link simbólico no home do usuário /var/www/members/{username}/{subdomain}
            symlink_path = os.path.join(instance.member.get_home_directory_path(), instance.subdomain)
            if not os.path.exists(symlink_path):
                subprocess.run(['sudo', 'ln', '-s', subdomain_dir, symlink_path], check=True)
                subprocess.run(['sudo', 'chown', '-h', f'{instance.member.username}:{instance.member.username}', symlink_path], check=True)
                print(f"Created symlink: {symlink_path} -> {subdomain_dir}")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Error creating subdomain directory, symlink, or copying index.html: {e}")

@receiver(pre_delete, sender=Domain)
def exclude_subdomain_linux(sender, instance, **kwargs):
    user_home_directory = instance.member.get_home_directory_path()
    symlink_path = os.path.join(user_home_directory, instance.subdomain)
    subdomain_dir = instance.get_subdomain_directory()

    try:
        if os.path.exists(symlink_path):
            subprocess.run(['sudo', 'rm', '-rf', symlink_path], check=True)
            print(f"Removed symlink: {symlink_path}")

        if os.path.exists(subdomain_dir):
            subprocess.run(['sudo', 'rm', '-rf', subdomain_dir], check=True)
            print(f"Directory {subdomain_dir} removed successfully.")
        else:
            print(f"Directory {subdomain_dir} does not exist.")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Error deleting symlink or subdomain directory: {e}")
