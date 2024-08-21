from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
import os

def calculate_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255, unique=True)
    uid = models.IntegerField(null=True, blank=True)
    gid = models.IntegerField(null=True, blank=True)
    home_directory = models.CharField(max_length=255)
    shell = models.CharField(max_length=100, default='/bin/sh')
    group = models.CharField(max_length=150, default='www-data')
    comment = models.CharField(max_length=255, default='User Web Data Manager')
    last_login = models.DateTimeField(null=True, blank=True)
    account_expiry = models.DateTimeField(null=True, blank=True)
    password_expiry = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    inactive = models.BooleanField(default=False)
    sudo_access = models.BooleanField(default=False)
    max_storage_mb = models.IntegerField(default=500)
    current_storage_kb = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['uid']),
            models.Index(fields=['gid']),
        ]
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_home_directory_path(self):
        """
        Retorna o caminho completo do diretório home do usuário Linux.
        Exemplo: /var/www/members/{username}/
        """
        return os.path.join('/var/www/members/', self.username)

    def update_storage_usage(self):
        """
        Atualiza o uso de armazenamento do membro e armazena em cache.
        """
        home_dir = self.get_home_directory_path()
        if os.path.exists(home_dir):
            storage_kb = calculate_directory_size(home_dir) // 1024
            cache_key = f'member:{self.id}:storage_kb'
            cache.set(cache_key, storage_kb, timeout=300)  # Cache por 5 minutos
            self.current_storage_kb = storage_kb
            self.save()

    def get_cached_storage_usage(self):
        """
        Retorna o uso de armazenamento a partir do cache, se disponível.
        """
        cache_key = f'member:{self.id}:storage_kb'
        storage_kb = cache.get(cache_key)

        if storage_kb is None:
            self.update_storage_usage()
            storage_kb = self.current_storage_kb

        return storage_kb

    def has_exceeded_storage_limit(self):
        """
        Verifica se o membro excedeu seu limite de armazenamento.
        """
        return self.get_cached_storage_usage() > (self.max_storage_mb * 1024)


class MemberAwareModel(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Domain(MemberAwareModel):
    subdomain = models.CharField(max_length=255, unique=True)
    requests = models.IntegerField(default=0)
    visitors = models.IntegerField(default=0)
    files_count = models.IntegerField(default=0)
    data_usage_kb = models.IntegerField(default=0)

    def __str__(self):
        return self.subdomain

    def get_subdomain_directory(self):
        """
        Retorna o caminho para o diretório do subdomínio em /var/www/<subdomain>
        """
        return os.path.join('/var/www/', self.subdomain)

    def update_files_and_data_usage(self):
        """
        Atualiza a contagem de arquivos e o uso de dados para o subdomínio e armazena em cache.
        """
        subdomain_dir = self.get_subdomain_directory()
        if os.path.exists(subdomain_dir):
            files_count = len([f for f in os.listdir(subdomain_dir) if os.path.isfile(os.path.join(subdomain_dir, f))])
            data_usage_kb = calculate_directory_size(subdomain_dir) // 1024

            cache.set(f'domain:{self.id}:files_count', files_count, timeout=300)  # Cache por 5 minutos
            cache.set(f'domain:{self.id}:data_usage_kb', data_usage_kb, timeout=300)

            self.files_count = files_count
            self.data_usage_kb = data_usage_kb
            self.save()

    def get_cached_files_count(self):
        """
        Retorna a contagem de arquivos a partir do cache, se disponível.
        """
        cache_key = f'domain:{self.id}:files_count'
        files_count = cache.get(cache_key)

        if files_count is None:
            self.update_files_and_data_usage()
            files_count = self.files_count

        return files_count

    def get_cached_data_usage(self):
        """
        Retorna o uso de dados a partir do cache, se disponível.
        """
        cache_key = f'domain:{self.id}:data_usage_kb'
        data_usage_kb = cache.get(cache_key)

        if data_usage_kb is None:
            self.update_files_and_data_usage()
            data_usage_kb = self.data_usage_kb

        return data_usage_kb

    class Meta:
        indexes = [
            models.Index(fields=['subdomain']),
        ]
        verbose_name = "Subdominio"
        verbose_name_plural = "Subdominios"
        ordering = ['subdomain']
