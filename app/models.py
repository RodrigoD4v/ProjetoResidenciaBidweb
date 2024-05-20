from django.db import models

class TestConfig(models.Model):
    url = models.TextField()

    def __str__(self):
        return self.url


class TestResult(models.Model):
    STATUS_CHOICES = [
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
    ]
    
    test_config = models.ForeignKey(TestConfig, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class Vulnerability(models.Model):
    TIPO_CHOICES = [
        ('SQL Injection', 'SQL Injection'),
        ('XSS', 'XSS'),
        ('Command Injection', 'Command Injection'),
        ('Local File Inclusion', 'Local File Inclusion'),
        ('HTTP Header Injection', 'HTTP Header Injection'),
        
    ]
    
    IMPACTO_CHOICES = [
        ('Baixo', 'Baixo'),
        ('Médio', 'Médio'),
        ('Alto', 'Alto'),
    ]
    
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descrição = models.TextField()
    impacto = models.CharField(max_length=10, choices=IMPACTO_CHOICES)

