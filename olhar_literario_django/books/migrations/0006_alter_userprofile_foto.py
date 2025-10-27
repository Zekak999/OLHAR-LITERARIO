# Generated migration for GitHub storage on foto field

from django.db import migrations, models
import books.storage


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_capa_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='foto',
            field=models.ImageField(blank=True, null=True, storage=books.storage.GitHubMediaStorage(), upload_to='profile_photos/'),
        ),
    ]
