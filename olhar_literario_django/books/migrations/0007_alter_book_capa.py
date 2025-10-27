# Generated migration for GitHub storage on capa field

from django.db import migrations, models
import books.storage


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_userprofile_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='capa',
            field=models.ImageField(blank=True, help_text='Deixe em branco se usar o link do Google Drive acima', null=True, storage=books.storage.GitHubMediaStorage(), upload_to='book_covers/', verbose_name='Capa (Upload - Opcional)'),
        ),
    ]
